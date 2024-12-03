import React, { useEffect, useState } from "react";
import { ReactReader } from "react-reader";

const EpubReader: React.FC = () => {
  const [location, setLocation] = useState<string | number>(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  //   const audioRef = useRef<HTMLAudioElement | null>(null);

  const handleLocationChanged = (epubcfi: string) => {
    setLocation(epubcfi);

    // Extraire le numéro de page à partir de epubcfi
    const pageMatch = epubcfi.match(/\/(\\d+)/);
    if (pageMatch && pageMatch[1]) {
      const newPage = parseInt(pageMatch[1], 10);
      if (newPage !== currentPage) {
        setCurrentPage(newPage);
      }
    }
  };

  useEffect(() => {
    const url = localStorage.getItem("uploadedFileUrl");
    if (url) {
      setFileUrl(url);
    }
  }, []);

  return (
    <>
      <button onClick={() => window.location.href = '/'}>Back to Homepage</button>
      <div style={{ height: "100vh" }}>
        <ReactReader
          url={fileUrl}
          location={location}
          locationChanged={handleLocationChanged}
        />
        <audio autoPlay src="/music.wav" loop />
      </div>
    </>
  );
};

export default EpubReader;
