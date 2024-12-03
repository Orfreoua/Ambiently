import React, { useState } from "react";
import { ReactReader } from "react-reader";

const EpubReader: React.FC = () => {
  const [location, setLocation] = useState<string | number>(0);
  const [currentPage, setCurrentPage] = useState(0);
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
  return (
    <div style={{ height: "100vh" }}>
      <ReactReader
        url="/prince.epub"
        location={location}
        locationChanged={handleLocationChanged}
      />
      <audio autoPlay src="/music.wav" loop />
    </div>
  );
};

export default EpubReader;
