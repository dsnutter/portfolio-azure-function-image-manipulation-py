function ConvertImageToBase64 {
    param(
        [string]$imagePath
    )

    $image = [System.IO.File]::ReadAllBytes($imagePath)
    $base64 = [System.Convert]::ToBase64String($image)

    # make sure base64 is a multiple of 4 for valid encoding
    $padding = 0
    if ($base64.Length % 4 -ne 0) {
        $padding = 4 - ($base64.Length % 4)
    }
    $base64 += [System.String]::new('=', $padding)

    return $base64
}

function ConvertBase64ToImage {
    param(
        [string]$base64,
        [string]$outputPath
    )

    $image = [System.Convert]::FromBase64String($base64)
    [System.IO.File]::WriteAllBytes($outputPath, $image)
}

