$docxPath = "C:\Users\RATNAM\.gemini\antigravity\scratch\water-potability-svm\PROJECT_REPORT_URLA_ENOCH_PHILIP.docx"
$pdfPath = "C:\Users\RATNAM\.gemini\antigravity\scratch\water-potability-svm\PROJECT_REPORT_URLA_ENOCH_PHILIP.pdf"

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($docxPath)
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)
    $doc.Close()
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Output "PDF created successfully at: $pdfPath"
} catch {
    Write-Output "Error exporting to PDF: $_"
}
