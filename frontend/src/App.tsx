import { BrowserRouter, Routes, Route } from "react-router-dom";
import EpubUploader from "./components/EpubUploader";
import "./index.css";
import EpubReader from "./components/EpubReader";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<EpubUploader />} />
        <Route path="/reader" element={<EpubReader />} />
        <Route path="*" element={<EpubUploader />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
