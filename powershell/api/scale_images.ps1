#
# script resize image from a folder using an api endpoint via multipart/form-data and application/json types
#

# check for command line arguments
if ($args.Length -lt 4) {
    Write-Host "Usage: sclae_images.ps1 <endpoint_url> <imageFolderPath> <contenttype> <scale>"
    Write-Host "Content types are: multipart or json"
    Write-Host "Scale is a positive or negative integer"
    exit
}

# include functions
. ./functions.ps1
. ../utility/functions.ps1

#
# CONFIGURATION
#
# this is a sample key and is not used in the actual deployment
$security_key = "abc123"

# this is the local docker url of the api
# $url = "http://localhost:8080/api/v1/scale"
$url = $args[0]

# the images to process
# $imageFile = "$scriptPath/../../images/originals/1.jpg"
$imageFolder = $args[1]

# how to process the images via the apu
$content_type = $args[2]

# the scale to use
$scale = $args[3]

# get all paths to images in folder
$imageFiles = Get-ChildItem -Path $imageFolder -Recurse -Include *.jpg, *.jpeg, *.png

# get current path script is running in
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent


#
# EXECUTE mulitpart/form-data
#
if ($content_type -eq "multipart") {
    # process each image
    foreach ($imageFile in $imageFiles) {
        Write-Host ""
        $result = GetScaledImage_ViaMultipart $imageFile $url $security_key $scale "$scriptPath\\results"
        $original = $result.original_dimensions.width, $result.original_dimensions.height
        $scaled = $result.scaled_dimensions.width, $result.scaled_dimensions.height

        # print response
        Write-Host "Original dimensions are: " $original[0] "x" $original[1]
        Write-Host "Scaled dimensions are: " $scaled[0] "x" $scaled[1]
        Write-Host ""
    }
}
#
# EXECUTE application/json
#
elseif ($content_type -eq "json") {
    # process each image
    foreach ($imageFile in $imageFiles) {
        Write-Host ""
        $result = GetScaledImage_ViaJson $imageFile $url $security_key $scale "$scriptPath\\results"
        $original = $result.original_dimensions.width, $result.original_dimensions.height
        $scaled = $result.scaled_dimensions.width, $result.scaled_dimensions.height

        # print response
        Write-Host "Original dimensions are: " $original[0] "x" $original[1]
        Write-Host "Scaled dimensions are: " $scaled[0] "x" $scaled[1]
        Write-Host ""
    }
}

Write-Host "Done."