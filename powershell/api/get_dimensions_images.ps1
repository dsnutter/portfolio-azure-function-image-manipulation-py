#
# script get dimensions from api endpoint via multipart/form-data and application/json types
#

# check for command line arguments
if ($args.Length -lt 1) {
    Write-Host "Usage: get_dimensions_image.ps1 <enpoint_url> <imageFolderPath> <contenttype>"
    Write-Host "Content types are: multipart or json"
    exit
}

# include functions
. ../utility/functions.ps1

#
# CONFIGURATION
#
# this is a sample key and is not used in the actual deployment
$env:security_key = "abc123"

# this is the local docker url of the api
# $url = "http://localhost:8080/api/v1/dimensions"
$url = $args[0]

# the images to process
# $imageFile = "$scriptPath/../../images/originals/1.jpg"
$imageFolder = $args[1]

# how to process the images via the apu
$content_type = $args[2]

# get all paths to images in folder
$imageFiles = Get-ChildItem -Path $imageFolder -Recurse -Include *.jpg, *.jpeg, *.png

#
# EXECUTE mulitpart/form-data
#
if ($content_type -eq "multipart") {
    # process each image
    foreach ($imageFile in $imageFiles) {
        Write-Host ""
        $width, $height = GetImageDimensions_ViaMultiPart $imageFile $url $env:security_key

        # print response
        Write-Host "Dimensions are: Width: $width, Height: $height"
        Write-Host ""
    }
}
elseif ($content_type -eq "json") {
    #
    # EXECUTE application/json
    #
    # process each image
    foreach ($imageFile in $imageFiles) {
        Write-Host ""
        $width, $height = GetImageDimensions_ViaJson $imageFile $url $env:security_key

        # print response
        Write-Host "Dimensions are: Width: $width, Height: $height"
        Write-Host ""
    }
}

Write-Host "Done."