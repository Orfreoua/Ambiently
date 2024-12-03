import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";

interface DropZoneProps {
  onFilesDrop: (files: File[]) => void;
}

const DropZone: React.FC<DropZoneProps> = ({ onFilesDrop }) => {
  const [isHovered, setIsHovered] = useState(false);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      onFilesDrop(acceptedFiles);
    },
    [onFilesDrop]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/epub+zip": [".epub"],
    },
  });

  return (
    <motion.div
      {...getRootProps()}
      className={`p-10 border-2 border-dashed rounded-lg text-center cursor-pointer transition-all relative overflow-hidden ${
        isDragActive
          ? "border-cyan-300"
          : isHovered
          ? "border-white"
          : "border-white border-opacity-50"
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <input {...getInputProps()} />
      <AnimatePresence>
        {isDragActive && (
          <motion.div
            className="absolute inset-0 bg-cyan-300 bg-opacity-20"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />
        )}
      </AnimatePresence>
      <motion.div
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {isDragActive ? (
          <p className="text-cyan-300 font-semibold text-lg">
            Déposez les fichiers ici ...
          </p>
        ) : (
          <p className="text-white text-lg">
            Glissez et déposez des fichiers EPUB ici, ou cliquez pour
            sélectionner des fichiers
          </p>
        )}
      </motion.div>
      <motion.div
        className="mt-4 flex justify-center items-center"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: "spring", stiffness: 300, damping: 20 }}
      >
        <svg
          className="w-12 h-12 text-white opacity-70"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      </motion.div>
    </motion.div>
  );
};

export default DropZone;
