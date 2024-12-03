import React, { useState } from "react";
import DropZone from "./DropZone";

interface FilePreview {
  file: File;
  name: string;
  size: number;
}

const EpubUploader: React.FC = () => {
  const [file, setFile] = useState<FilePreview | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const handleFilesDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const newFile = acceptedFiles[0];
      setFile({
        file: newFile, // Store the actual File object for upload
        name: newFile.name,
        size: newFile.size,
      });
    }
  };

  const removeFile = () => {
    setFile(null);
  };

  const uploadFile = async () => {
    console.log("Upload file");
    if (!file || !file.file) return; // Ensure a valid file is available

    setIsUploading(true);
    setUploadStatus(null);

    const formData = new FormData();
    formData.append("file", file.file); // Use the actual File object

    console.log("FormData:");
    for (const [key, value] of formData.entries()) {
      console.log(`${key}:`, value);
    }

    try {
      const response = await fetch("http://127.0.0.1:3000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setUploadStatus("Fichier envoyé avec succès !");
        setFile(null); // Clear the file on success
        const data = await response.json();
        localStorage.setItem("uploadedFileUrl", data.data.url);
        window.location.href = "/reader";
      } else {
        setUploadStatus("Erreur lors de l'envoi du fichier.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      setUploadStatus("Erreur de connexion au serveur.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-400 via-cyan-500 to-blue-500 animate-gradient py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-white mb-2">
          Ambiantly
        </h1>
        <p className="text-xl text-center text-white mb-8">
          Votre bibliothèque EPUB personnelle
        </p>
        <div className="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-xl p-8 shadow-lg border border-white border-opacity-20">
          <DropZone onFilesDrop={handleFilesDrop} />
          {file && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4 text-white">
                Fichier sélectionné :
              </h2>
              <div className="bg-white bg-opacity-20 rounded-lg shadow-lg overflow-hidden mb-4 p-4 flex justify-between items-center">
                <div>
                  <p className="font-medium text-white">{file.name}</p>
                  <p className="text-sm text-white text-opacity-70">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <button
                  onClick={removeFile}
                  className="text-red-500 hover:text-red-100 transition-colors"
                >
                  Supprimer
                </button>
              </div>
              <button
                onClick={uploadFile}
                disabled={isUploading}
                className="w-full bg-cyan-500 hover:bg-cyan-600 text-white font-bold py-2 px-4 rounded transition-colors disabled:opacity-50"
              >
                {isUploading ? "Envoi en cours..." : "Envoyer le fichier"}
              </button>
              {uploadStatus && (
                <p
                  className={`mt-4 text-center ${
                    uploadStatus.includes("succès")
                      ? "text-green-300"
                      : "text-red-500"
                  }`}
                >
                  {uploadStatus}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EpubUploader;
