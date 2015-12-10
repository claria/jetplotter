<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>
<!DOCTYPE html>
<html>
<head>
<title>Plot Overview</title>
<style type="text/css">
.plot {
  display: inline-block;
  margin-left: 10px;
  margin-right: 10px;
}
h3  h1 {
  margin-bottom:5px;
}
</style>
</head>
<body>
<h1>Plot overview:</h1>
<p><a href="../">folder up</a></p>
<?php
  $allplots = glob('*.png');
  $allsubnames = array();
  foreach($allplots as $filename) {
    $baseplotname = basename($filename);
    // $splitname  = explode("_", $baseplotname, -1);
    // $subname = implode("_", $splitname);
    $subname = substr($filename, 0, strrpos($filename, "_"));
    $allsubnames[] = $subname;
  }
  $uniqueplots = array_unique($allsubnames, SORT_REGULAR);
?>
<?php 
function sort_datewise($x, $y) {
    $t1tmp = explode("_", pathinfo($x)['filename']);
    $t1 = strtotime(end($t1tmp));
    $t2tmp = explode("_", pathinfo($y)['filename']);
    $t2 = strtotime(end($t2tmp));
    return $t2 -$t1;
}    
foreach($uniqueplots as $uniqueplot): 
  echo "<div class=\"plot\">";
  echo "<h3>" . $uniqueplot . "</h3>";
  $allversions = array_filter($allplots, function ($var) use(&$uniqueplot) { return ($uniqueplot === substr($var, 0, strrpos($var, "_"))); });
  usort($allversions, 'sort_datewise');
  if (sizeof($allversions) > 1) {
  foreach($allversions as $key=>$plotfilename): 
    echo "[<a title=" . $plotfilename . " href=" . $plotfilename . ">" . $key . "</a>]";
  endforeach;
  }
  echo "<div>";
?>
          <a href="<?php echo $allversions[0] ?>"><img src="<?php echo $allversions[0] ?>" height="300" title="<?php echo $allversions[0] ?>" alt="plot missing"></a>
      </div>
    </div>
<?php 
endforeach;
?>
</body>
</html>

