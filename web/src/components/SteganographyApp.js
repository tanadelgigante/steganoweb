import React, { useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { AlertCircle, Upload } from 'lucide-react';  // Add Upload to the import
import { Alert, AlertDescription } from '../components/ui/alert';

const SteganographyApp = () => {
  // State management for file handling and UI
  const [inputImage, setInputImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState('');
  const [isEncoding, setIsEncoding] = useState(true);
  const [processedImage, setProcessedImage] = useState(null);
  const [originalFormat, setOriginalFormat] = useState(null);
  const fileInputRef = useRef(null);

  // Handle file selection
  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setInputImage(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      setStatus('');
      // Extract format from MIME type (e.g., 'image/jpeg' -> 'jpg')
      const format = file.type.split('/')[1].replace('jpeg', 'jpg');
      setOriginalFormat(format);
    } else {
      setStatus('Please select a valid image file');
    }
  };

  // Trigger file input click
  const handleBrowseClick = () => {
    fileInputRef.current.click();
  };

  // Handle encode/decode operations
  const handleOperation = async () => {
    console.log('Starting operation:', isEncoding ? 'encode' : 'decode');
    try {
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Image = reader.result;
        const endpoint = isEncoding ? '/encode' : '/decode';
        
        // Modifica qui per usare direttamente l'URL dell'API
        const apiUrl = `${process.env.REACT_APP_API_URL || 'http://192.168.188.120:71'}${endpoint}`;
        console.log('Calling API at:', apiUrl);
        
        try {
          const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',  // Add this line for CORS credentials
            body: JSON.stringify({
              image: base64Image,
              message: isEncoding ? message : undefined,
            }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const data = await response.json();
          console.log('Response data:', data);
        
          if (data.error) {
            setStatus(`Error: ${data.error}`);
            return;
          }
  
          if (isEncoding) {
            setProcessedImage(data.image);
            setPreviewUrl(data.image);
            setStatus('Message encoded successfully!');
          } else {
            setMessage(data.message);
            setStatus('Message decoded successfully!');
          }
        } catch (error) {
          console.error('API call failed:', error);
          setStatus(`Error calling API: ${error.message}`);
        }
      };
      
      reader.readAsDataURL(inputImage);
    } catch (error) {
      console.error('Operation failed:', error);
      setStatus(`Error: ${error.message}`);
    }
  };

  const handleDownload = () => {
    if (processedImage) {
      const link = document.createElement('a');
      link.href = processedImage;
      link.download = `stegano_${isEncoding ? 'encoded' : 'decoded'}_image.${originalFormat || 'png'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            SteganoWeb
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Image Preview */}
          <div className="relative h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Preview"
                className="max-h-full max-w-full object-contain"
              />
            ) : (
              <div className="text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600">No image selected</p>
              </div>
            )}
          </div>

          {/* File Input */}
          <div className="space-y-2">
            <Input
              type="file"
              ref={fileInputRef}
              onChange={handleFileSelect}
              className="hidden"
              accept="image/*"
            />
            <Button 
              onClick={handleBrowseClick}
              className="w-full"
              variant="outline"
            >
              Browse Image
            </Button>
          </div>

          {/* Message Input/Output */}
          <Textarea
            placeholder={isEncoding ? "Enter message to encode..." : "Decoded message will appear here..."}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="h-24"
          />

          {/* Operation Controls */}
          <div className="flex gap-4">
            <Button
              className="flex-1"
              variant={isEncoding ? "default" : "outline"}
              onClick={() => setIsEncoding(true)}
            >
              Encode Mode
            </Button>
            <Button
              className="flex-1"
              variant={!isEncoding ? "default" : "outline"}
              onClick={() => setIsEncoding(false)}
            >
              Decode Mode
            </Button>
          </div>

          <Button 
            onClick={handleOperation} 
            className="w-full"
          >
            {isEncoding ? 'Encode Message' : 'Decode Message'}
          </Button>

          {processedImage && isEncoding && (
            <Button 
              onClick={handleDownload}
              className="w-full bg-green-600 hover:bg-green-700"
            >
              Download Encoded Image
            </Button>
          )}

          {/* Status Messages */}
          {status && (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{status}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default SteganographyApp