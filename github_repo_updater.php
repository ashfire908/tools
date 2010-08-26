<?php
// GitHub Repo Updater Service Hook

// Settings

// Paths to Git Repos
$repos = array();
$repos['repo_name'] = '/path/to/git/repo/';

// Log files
$update_log_path = 'github_update.log';
$error_log_path = 'github_error.log';

// Initial variables
//$user_id = posix_geteuid();
$start_dir = getcwd();
$return_code = null;
$git_output = array();
$repo = '-';


// Process incoming data
if ($_POST['payload'] == null) {
    $update = false;
    $error = 'No data received from http client.';
} else {
    $payload = json_decode($_POST['payload']);
    $repo = $payload->{'repository'}->{'name'};
    if (! array_key_exists($repo, $repos)) {
        $update = false;
        $error = "No path for repository ${repo} given.";
    } else {
        $folder = $repos[$repo];
        chdir($folder);
        
        exec('git pull', $git_output, $return_code);
        if ($return_code != 0) {
            $update = false;
            $error = 'Return Code: ' . $return_code . '\nGit Output:\n' . $git_output;
        } else {
            $update = true;
        }
    }
}
// Output page
// In case short tag is enabled
echo '<?xml version="1.0" encoding="UTF-8" ?>';?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Git Update <?php
if ($update == true) {
  echo 'Sucessful';
} else {
  echo 'Failed';
}?></title>
</head>
<body>
<?php if ($update == true) {
?>  <h1>Update Sucessful</h1>
    
    <p>The Git update for the repo <a href="<?php echo $payload->{'repository'}->{'url'};?>" title="GitHub Repo for <?php echo $repo; ?>"><?php echo $repo; ?></a> was completed sucessfully.</p>
<?php
} else {
?>  <h1>Update Failed</h1>
    
    <p>The Git updated failed. The error was:
      <code><?php echo $error; ?></code>
    </p>
<?php
}?>
</body>
</html>
<?php 
chdir($start_dir);
$update_log = fopen($update_log_path, 'a');
$date = date(DateTime::ISO8601);
$log_output = "${date} - Repo ${repo} Update ";
if ($update == true) { 
  $log_output .= "Sucessful\n";
  $owner_name = $payload->{'repository'}->{'owner'}->{'name'};
  $owner_email = $payload->{'repository'}->{'owner'}->{'email'};
  $ref = $payload->{'ref'};
  $before = $payload->{'before'};
  $after = $payload->{'after'};
  $log_output .= "${date} - Repo ${repo} (owned by ${owner_name} <${owner_email}>) updated ref ${ref} from ${before} to ${after}.\n";
  fwrite($update_log, $log_output);
  fclose($update_log);
} else {
  $log_output .= "Failed\n";
  $error_output = "${date} - (${repo}) ${error}\n";
  if ($return_code != null) {
    $error_output .= "${date} - (${repo}) Return Code ${return_code}\n";
  }
  foreach($git_output as $line) {
    $error_output .= "${date} - (${repo}) ${line}\n";
  }
  fwrite($update_log, $log_output);
  fclose($update_log);
  $error_log = fopen($error_log_path, 'a');
  fwrite($error_log, $error_output);
  fclose($error_log);
}

?>
