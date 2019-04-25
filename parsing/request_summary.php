<?php

function print_help()
{
    $help = "usage: request_summary.php [-h] [--smmry_api_key KEY] [--input_dir INPUT_DIR] [-output_dir OUTPUT_DIR]";
    $help .= "arguments:\n";
    $help .= "-h, --help\t\tshow this help message and exit\n";
    $help .= "--smmry_api_key KEY, -k KEY\n\t\tYour SMMRY API key. For more info, visit https://smmry.com/api\n";
    $help .= "--input_dir INPUT_DIR, -i INPUT_DIR\n\t\tPath to directory of text files for summarization.\n";
    $help .= "--output_dir OUTPUT_DIR, -o OUTPUT_DIR\n\t\tPath to output directory.\n\n";
    echo $help;
    exit(1);
}

function format_optcode($optcode)
{
    return str_replace(":", "", $optcode);
}

function arg_check()
{
    $shortopts = array(
        "h",
        "k:",
        "i:",
        "o:",
    );
    $longopts = array(
        "help",
        "api_key:",
        "input_dir:",
        "output_dir:",
    );
    $opts = getopt(implode($shortopts), $longopts);

    if (array_key_exists("help", $opts) || array_key_exists("h", $opts) || count($opts) !== 3) {
        print_help();
    }

    $options = array();

    for ($i = 0; $i < count($longopts); $i++) {
        $short_opt = format_optcode($shortopts[$i]);
        $long_opt = format_optcode($longopts[$i]);

        $has_short_opt = array_key_exists($short_opt, $opts);
        $has_long_opt = array_key_exists($long_opt, $opts);

        if ($has_short_opt && $has_long_opt) {
            print_help();
        } elseif ($has_short_opt && !$has_long_opt) {
            $options[] = $opts[$short_opt];
        } elseif (!$has_short_opt && $has_long_opt) {
            $options[] = $opts[$long_opt];
        }
    }

    return $options;
}

list($api_key, $input_dir, $output_dir) = arg_check();

// Open a directory, and read its contents
$files = scandir($input_dir);
if (is_array($files)) {
    foreach ($files as $key => $value) {
        $infile = $input_dir . "/" . $value;
        $outfile = $output_dir . "/" . $value;
        if (is_file($infile)) {
            $text = file_get_contents($infile);
            $ch = curl_init("http://api.smmry.com/&SM_API_KEY=" . $api_key . "&SM_WITH_BREAK");
            curl_setopt($ch, CURLOPT_HTTPHEADER, array("Expect:"));
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, "sm_api_input=" . $text);
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 20);
            curl_setopt($ch, CURLOPT_TIMEOUT, 20);
            $return = json_decode(curl_exec($ch), true);
            curl_close($ch);

            $summary = str_replace("[BREAK] ", "\n\n", $return['sm_api_content']);
            $summary_file = fopen($outfile, "w");
            fwrite($summary_file, $summary);
            fclose($summary_file);
        }
    }
}
