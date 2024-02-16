#
# script calls base64 image conversion functions with parameters passed via command line
# script must be run from the powershell directory
#

# check for command line arguments
if ($args.Length -lt 1) {
    Write-Host "Usage: convert-image-base64-from.ps1 <imageName>"
    Write-Host "Images are pulled from the test-images/base64decode directory and output to test-images/base64decode/decoded"
    exit
}

# include functions
. ./functions.ps1

# get image name from command line
$imageBase64 = $args[0]

# get current filesystem location
$scriptPath = Split-Path -parent $MyInvocation.MyCommand.Definition

# paths
$imageBase64Path = $scriptPath + '/../../images/base64decode/' + $imageBase64
$outputPath = $scriptPath + '/../../images/base64decode/decoded/' + $imageBase64.Replace('.base64.txt', '')

# write image to file
ConvertBase64ToImage $imageBase64Path $outputPath



