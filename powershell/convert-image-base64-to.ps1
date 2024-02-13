#
# script calls base64 image conversion functions with parameters passed via command line
# script must be run from the powershell directory
#

# check for command line arguments
if ($args.Length -lt 1) {
    Write-Host "Usage: convert-image-base64-to.ps1 <imageName>"
    Write-Host "Images are pulled from the test-images/originals directory and output to test-images/base64"
    exit
}

# include functions
. ./functions.ps1

# get image name from command line
$imageName = $args[0]

# get current filesystem location
$scriptPath = Split-Path -parent $MyInvocation.MyCommand.Definition

# paths
$imagePath = $scriptPath + '/../test_images/originals/' + $imageName
$outputPath = $scriptPath + '/../test_images/base64/' + $imageName + '.base64.txt'

# convert image to base64
$base64 = ConvertImageToBase64 $imagePath

# write base64 string to file
Set-Content -Path $outputPath -Value $base64


