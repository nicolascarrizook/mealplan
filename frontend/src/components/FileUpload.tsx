import { useState, useCallback } from 'react'
import { Upload, FileText, Image, Table, X, Download, Eye, Cpu } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { useToast } from "@/components/ui/use-toast"
import { mealPlanService } from '@/services/api'
import type { ControlPatientData } from '@/types'

interface FileUploadProps {
  onDataExtracted: (data: Partial<ControlPatientData>) => void
}

export function FileUpload({ onDataExtracted }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [extractionMethod, setExtractionMethod] = useState<'ocr' | 'vision' | 'auto'>('auto')
  const { toast } = useToast()

  const acceptedTypes = {
    'application/pdf': { icon: FileText, color: 'text-red-500' },
    'application/vnd.ms-excel': { icon: Table, color: 'text-green-500' },
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': { icon: Table, color: 'text-green-500' },
    'text/csv': { icon: Table, color: 'text-green-500' },
    'image/jpeg': { icon: Image, color: 'text-blue-500' },
    'image/jpg': { icon: Image, color: 'text-blue-500' },
    'image/png': { icon: Image, color: 'text-blue-500' },
  }

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      handleFileSelect(files[0])
    }
  }, [])

  const handleFileSelect = async (file: File) => {
    if (!acceptedTypes[file.type as keyof typeof acceptedTypes]) {
      toast({
        title: "Tipo de archivo no soportado",
        description: "Por favor, sube un archivo PDF, Excel, CSV o imagen (JPG/PNG)",
        variant: "destructive",
      })
      return
    }

    setUploadedFile(file)
    setIsUploading(true)

    try {
      // Only use selected method for images
      const method = file.type.startsWith('image/') ? extractionMethod : 'auto'
      const response = await mealPlanService.uploadControlFile(file, method)
      
      if (response.success) {
        const methodUsed = response.method_used === 'vision' ? 'Visión AI' : 
                          response.method_used === 'ocr' ? 'OCR' : 'Estándar'
        
        toast({
          title: "Archivo procesado exitosamente",
          description: `${response.message} (Método: ${methodUsed})`,
        })
        
        // Pass extracted data to parent component
        onDataExtracted(response.data)
      }
    } catch (error) {
      toast({
        title: "Error al procesar el archivo",
        description: "Hubo un problema al extraer los datos del archivo",
        variant: "destructive",
      })
    } finally {
      setIsUploading(false)
    }
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFileSelect(files[0])
    }
  }

  const removeFile = () => {
    setUploadedFile(null)
  }

  const downloadTemplate = () => {
    mealPlanService.downloadControlTemplate()
  }

  const getFileIcon = () => {
    if (!uploadedFile) return null
    const fileInfo = acceptedTypes[uploadedFile.type as keyof typeof acceptedTypes]
    if (!fileInfo) return <FileText className="h-12 w-12" />
    
    const Icon = fileInfo.icon
    return <Icon className={`h-12 w-12 ${fileInfo.color}`} />
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Subir archivo de control anterior</h3>
            <Button
              variant="outline"
              size="sm"
              onClick={downloadTemplate}
              className="flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              Descargar plantilla Excel
            </Button>
          </div>

          {!uploadedFile ? (
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                isDragging ? 'border-primary bg-primary/5' : 'border-gray-300'
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-lg mb-2">
                Arrastra y suelta tu archivo aquí
              </p>
              <p className="text-sm text-gray-500 mb-4">
                o
              </p>
              <label htmlFor="file-upload">
                <Button asChild disabled={isUploading}>
                  <span>
                    Seleccionar archivo
                  </span>
                </Button>
                <input
                  id="file-upload"
                  type="file"
                  className="hidden"
                  accept=".pdf,.xlsx,.xls,.csv,.jpg,.jpeg,.png"
                  onChange={handleFileInputChange}
                  disabled={isUploading}
                />
              </label>
              <p className="text-xs text-gray-500 mt-4">
                Formatos soportados: PDF, Excel, CSV, JPG, PNG
              </p>
            </div>
          ) : (
            <div className="border rounded-lg p-4 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getFileIcon()}
                  <div>
                    <p className="font-medium">{uploadedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(uploadedFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                {!isUploading && (
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={removeFile}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </div>
              
              {/* Show extraction method options for images */}
              {uploadedFile.type.startsWith('image/') && !isUploading && (
                <div className="space-y-2">
                  <Label className="text-sm font-medium">Método de extracción:</Label>
                  <RadioGroup
                    value={extractionMethod}
                    onValueChange={(value) => setExtractionMethod(value as 'ocr' | 'vision' | 'auto')}
                  >
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="auto" id="auto" />
                      <Label htmlFor="auto" className="flex items-center gap-2 cursor-pointer">
                        <span className="text-purple-600">⚡</span>
                        Automático (Recomendado)
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="vision" id="vision" />
                      <Label htmlFor="vision" className="flex items-center gap-2 cursor-pointer">
                        <Eye className="h-4 w-4 text-blue-600" />
                        Visión AI (Más preciso)
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="ocr" id="ocr" />
                      <Label htmlFor="ocr" className="flex items-center gap-2 cursor-pointer">
                        <Cpu className="h-4 w-4 text-green-600" />
                        OCR (Más rápido)
                      </Label>
                    </div>
                  </RadioGroup>
                </div>
              )}
              
              {isUploading && (
                <div className="mt-4">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-primary h-2 rounded-full animate-pulse" style={{ width: '70%' }} />
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    {extractionMethod === 'vision' ? 'Analizando imagen con AI...' : 'Procesando archivo...'}
                  </p>
                </div>
              )}
            </div>
          )}

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">¿Cómo funciona?</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• <strong>PDF</strong>: Sube el plan anterior generado por el sistema</li>
              <li>• <strong>Excel/CSV</strong>: Usa nuestra plantilla para múltiples pacientes</li>
              <li>• <strong>Imagen</strong>: Toma una foto del plan anterior</li>
              <li className="ml-4">- <strong>Visión AI</strong>: Usa GPT-4 Vision para mejor precisión</li>
              <li className="ml-4">- <strong>OCR</strong>: Extracción rápida de texto tradicional</li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}