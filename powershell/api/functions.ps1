function CallImageApiJson {
    param(
        [string]$url,
        # body is hashtable
        [hashtable]$body,
        # azure function security key
        [string]$security_key
    )
    $method = "POST"

    $headers = @{
        "Content-Type" = "application/json"
        "x-functions-key" = "$security_key"
    }
    $json = $body | ConvertTo-Json

    $response = Invoke-RestMethod -Uri $url -Method $method -Headers $headers -Body $json
    return $response
}

function CallImageApiMultiPart {
    param(
        [string]$url,
        # form data is a hashtable
        [System.Collections.Hashtable]$formData,
        # azure function security key
        [string]$security_key
    )
    $method = "POST"

    $headers = @{
        "x-functions-key" = "$security_key"
    }

    $response = Invoke-RestMethod -Uri $url -ContentType "multipart/form-data" -Method $method -Headers $headers -Form $formData
    return $response
}
function GetImageDimensions_ViaMultiPart {
    param(
        [string]$imageFile,
        [string]$url,
        [string]$security_key
    )

    Write-Host "Getting image dimensions from api via multipart/form-data"
    Write-Host "for image: $imageFile"
    $file = Get-Item -Path $imageFile  
    
    # create form data
    $formData = @{
        image = $file 
    }
    
    try 
    {
        # call api
        $response = CallImageApiMultiPart $url $formData $security_key
        # $json_response = $response | ConvertTo-Json
        
        # parse response
        $width = $response.dimensions.width
        $height = $response.dimensions.height

        return $width, $height
    }
    catch 
    {
        Write-Host "Error calling api: $url"
        Write-Host "Is the endpoint running? Is the security key correct?"
        Write-Host "Error is: $_"
    }   
    return 0,0
}


function GetImageDimensions_ViaJson {
    param(
        [string]$imageFile,
        [string]$url,
        [string]$security_key
    )

    Write-Host "Getting image dimensions from api via JSON"
    Write-Host "for image: $imageFile"
    $file = ConvertImageToBase64 $imageFile
    
    # create form data
    $body = @{
        image = $file 
    }
    
    try 
    {
        # call api
        $response = CallImageApiJson $url $body $security_key
        # $json_response = $response | ConvertTo-Json
        
        # parse response
        $width = $response.dimensions.width
        $height = $response.dimensions.height

        return $width, $height
    }
    catch 
    {
        Write-Host "Error calling api: $url"
        Write-Host "Is the endpoint running? Is the security key correct?"
        Write-Host "Error is: $_"
    }
    return 0,0
}

function GetScaledImage_ViaMultipart {
    param(
        [string]$imageFile,
        [string]$url,
        [string]$security_key,
        [int]$scale,
        [string]$write_folder
    )

    Write-Host "Getting scaled image from api via multipart/form-data"
    Write-Host "for image: $imageFile"
    Write-Host "at scale: $scale"
    $file = Get-Item -Path $imageFile  
    
    # create form data
    $formData = @{
        image = $file
        scale = $scale
    }
    
    try 
    {
        # example response
        # "original_dimensions": {
        #     "width": 1936,
        #     "height": 2592
        # },
        # "scaled_dimensions": {
        #     "width": 968,
        #     "height": 1296
        # },
        # "scale": -2,
        # "img_scaled":

        # call api
        $response = CallImageApiMultiPart $url $formData $security_key
        #$json_response = $response | ConvertTo-Json
        #Write-Host $json_response
        
        # parse response
        $scaledImage = $response.img_scaled
        Write-Host "Scaled image length: $($scaledImage.Length)"

        $scaledImagePath = WriteImage_Custom $imageFile $scaledImage $write_folder

        return @{
            'scaled_image_filename' = $scaledImagePath
            'scaled_dimensions' = $response.scaled_dimensions
            'original_dimensions' = $response.original_dimensions
        }
    }
    catch 
    {
        Write-Host "Error calling api: $url"
        Write-Host "Is the endpoint running? Is the security key correct?"
        Write-Host "Error is: $_"
    }
    return @{}
}

function GetScaledImage_ViaJson {
    param(
        [string]$imageFile,
        [string]$url,
        [string]$security_key,
        [int]$scale,
        [string]$write_folder
    )

    Write-Host "Getting scaled image from api via JSON"
    Write-Host "for image: $imageFile"
    Write-Host "at scale: $scale"
    $file = ConvertImageToBase64 $imageFile
    
    # create form data
    $body = @{
        image = $file 
        scale = $scale
    }
    
    try 
    {
        # example response
        # "original_dimensions": {
        #     "width": 1936,
        #     "height": 2592
        # },
        # "scaled_dimensions": {
        #     "width": 968,
        #     "height": 1296
        # },
        # "scale": -2,
        # "img_scaled":

        # call api
        $response = CallImageApiJson $url $body $security_key
        # $json_response = $response | ConvertTo-Json
        
        # parse response
        $scaledImage = $response.img_scaled
        Write-Host "Scaled image length: $($scaledImage.Length)"

        $scaledImagePath = WriteImage_Custom $imageFile $scaledImage $write_folder

        return @{
            'scaled_image_filename' = $scaledImagePath
            'scaled_dimensions' = $response.scaled_dimensions
            'original_dimensions' = $response.original_dimensions
        }
    }
    catch 
    {
        Write-Host "Error calling api: $url"
        Write-Host "Is the endpoint running? Is the security key correct?"
        Write-Host "Error is: $_"
    }   
    return @{}
}

function WriteImage_Custom {
    param(
        [string]$imageFile,
        [string]$scaledImage,
        [string]$write_folder
    )

    # Split the file path on the backslash to get the filename with extension
    $filenameWithExtension = $imageFile -split '\\' | Select-Object -Last 1

    # Split the filename on the dot to get the filename without extension and the extension
    $filename = $filenameWithExtension -split '\.' | Select-Object -First 1
    $extension = $filenameWithExtension -split '\.' | Select-Object -Last 1
    # Write-Host "Filename without extension: $filename"
    # Write-Host "Extension: $extension"    
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"

    $outputPath = "$write_folder\\$timestamp-$filename-($scale).$extension"

    # write-host "Output path: $outputPath"

    # trim start of $scaledImage up to the first comma
    $scaledImage = $scaledImage.Substring($scaledImage.IndexOf(",")+1)

    # write-host "Scaled image length: $($scaledImage.Length)"

    $image = [System.Convert]::FromBase64String($scaledImage)
    [System.IO.File]::WriteAllBytes($outputPath, $image)

    Write-host "Writing scaled image to file system at: $outputPath"

    return $outputPath
}