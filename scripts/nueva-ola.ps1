param(
    [Parameter(Mandatory = $true)]
    [string]$Tema,

    [string]$Estado = "Ola abierta"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function New-ResearchSlug {
    param([string]$Text)

    $clean = $Text.Normalize([Text.NormalizationForm]::FormD)
    $chars = foreach ($char in $clean.ToCharArray()) {
        $category = [Globalization.CharUnicodeInfo]::GetUnicodeCategory($char)
        if ($category -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            $char
        }
    }

    $ascii = -join $chars
    $words = [regex]::Matches($ascii, "[A-Za-z0-9]+") | ForEach-Object {
        $value = $_.Value.ToLowerInvariant()
        if ($value.Length -eq 1) {
            $value.ToUpperInvariant()
        } else {
            $value.Substring(0, 1).ToUpperInvariant() + $value.Substring(1)
        }
    }

    return (-join $words)
}

function Insert-BeforeMarker {
    param(
        [string]$Path,
        [string]$Marker,
        [string]$Insertion
    )

    $content = Get-Content -LiteralPath $Path -Raw
    if (-not $content.Contains($Marker)) {
        throw "No se encontro el marcador '$Marker' en $Path."
    }

    $updated = $content.Replace($Marker, "$Insertion`r`n$Marker")
    Set-Content -LiteralPath $Path -Value $updated -Encoding UTF8
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$slug = New-ResearchSlug -Text $Tema

if ([string]::IsNullOrWhiteSpace($slug)) {
    throw "El tema no produjo un nombre de archivo valido."
}

$investigacion = "InvestigacionSobre$slug.md"
$resumen = "ResumenInvestigacionSobre$slug.md"

foreach ($path in @($investigacion, $resumen)) {
    if (Test-Path -LiteralPath $path) {
        throw "Ya existe $path. Elegi un tema mas especifico o renombra el archivo existente."
    }
}

@"
# Investigacion sobre $Tema

Fecha de apertura: $timestamp
Estado: $Estado
Resumen asociado: [$resumen]($resumen)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)

## Objetivo

Pendiente.

## Preguntas

- Pendiente.

## Fuentes

- Pendiente.

## Hallazgos

- Pendiente.

## Conclusion de esta ola

Pendiente.
"@ | Set-Content -LiteralPath $investigacion -Encoding UTF8

@"
# Resumen de la investigacion sobre $Tema

Fecha de apertura: $timestamp
Investigacion completa: [$investigacion]($investigacion)
Conclusion dinamica: [Conlusion.md](Conlusion.md)

## Resumen fuerte corto

Pendiente.

## Resumen fuerte ampliado

Pendiente.
"@ | Set-Content -LiteralPath $resumen -Encoding UTF8

$logEntry = "| $timestamp | $Tema | [$investigacion]($investigacion) | [$resumen]($resumen) | $Estado |"
Insert-BeforeMarker -Path "Investigacion.md" -Marker "## Estado actual del repositorio de investigacion" -Insertion $logEntry

$mapEntry = "- $timestamp | Alta de nueva ola: $Tema | Investigacion: [$investigacion]($investigacion) | Resumen: [$resumen]($resumen) | Conclusion vigente: [Conlusion.md](Conlusion.md)`r`n"
Insert-BeforeMarker -Path "InvestigacionMapa.md" -Marker "## Regla de actualizacion" -Insertion $mapEntry

@"
# Conlusion dinamica

Ultima actualizacion: $timestamp
Tema activo: $Tema

## Conlusion ejecutiva

Pendiente.

## Siguiente paso

Pendiente.
"@ | Set-Content -LiteralPath "Conlusion.md" -Encoding UTF8

Write-Host "Ola creada:"
Write-Host "  $investigacion"
Write-Host "  $resumen"
