import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const operations = {
  gray: { label: "Gri Dönüşüm", url: "/process/gray" },
  binary: { label: "Binary Dönüşüm", url: "/process/binary", params: ["threshold"] },
  rotate: { label: "Görüntü Döndürme", url: "/process/rotate", params: ["angle"] },
  crop: { label: "Görüntü Kırpma", url: "/process/crop", params: ["x", "y", "width", "height"] },
  zoom: { label: "Görüntü Yaklaştırma/Uzaklaştırma", url: "/process/zoom", params: ["scale", "center_x", "center_y"] },
  color: { label: "Renk Uzayı Dönüşümleri", url: "/process/color", params: ["mode"] },
  histogram: { label: "Histogram Germe/Genişletme", url: "/process/histogram", params: ["operation", "min_in", "max_in", "min_out", "max_out"] },
  arithmetic: { label: "Aritmetik İşlemler", url: "/process/arithmetic", params: ["arithmetic_op"] },
  contrast: { label: "Kontrast Azaltma", url: "/process/contrast", params: ["factor"] },
  median: { label: "Konvolüsyon (Median)", url: "/process/convolution", params: ["kernel_size"] },
  double_threshold: { label: "Çift Eşikleme", url: "/process/double_threshold", params: ["low_thresh", "high_thresh"] },
  edge: { label: "Kenar Algılama (Canny)", url: "/process/edge", params: ["threshold1", "threshold2"] },
  noise: { label: "Gürültü Ekleme", url: "/process/noise", params: ["salt_amount", "pepper_amount"] },
  denoise: { label: "Gürültü Temizleme", url: "/process/denoise", params: ["filter_type", "kernel_size"] },
  motion: { label: "Motion Filtresi", url: "/process/motion", params: ["kernel_size"] },
  morphology: { label: "Morfolojik İşlemler", url: "/process/morphology", params: ["morph_op", "kernel_size"] },
};

const defaultParams = {
  binary: { threshold: 127 },
  double_threshold: { low_thresh: 80, high_thresh: 160 },
  edge: { threshold1: 50, threshold2: 100 },
  crop: { x: 1, y: 1, width: 300, height: 400 },
  zoom: { scale: 1.5, center_x: 365, center_y: 700 },
  histogram: { operation: "stretch", min_in: 50, max_in: 200, min_out: 1, max_out: 255 },
  rotate: { angle: 90 },
  contrast: { factor: 0.5 },
  median: { kernel_size: 5 },
  denoise: { filter_type: "median", kernel_size: 3 },
  motion: { kernel_size: 20 },
  noise: { salt_amount: 0.2, pepper_amount: 0.2 },
  morphology: { morph_op: "open", kernel_size: 5 },
  arithmetic: { arithmetic_op: "multiply" },
  color: { mode: "hsv" },
};

function App() {
  const [selectedOperation, setSelectedOperation] = useState("gray");
  const [file, setFile] = useState(null);
  const [secondFile, setSecondFile] = useState(null);
  const [params, setParams] = useState(defaultParams[selectedOperation] || {});
  const [resultUrl, setResultUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleParamChange = (e) => {
    setParams({ ...params, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    if (!file) return;

   
    if (selectedOperation === "contrast") {
      const factorStr = params.factor?.toString().replace(",", ".");
      const factor = parseFloat(factorStr);
      if (isNaN(factor) || factor <= 0 || factor > 1) {
        alert("Lütfen kontrast için 0 ile 1 arasında bir değer girin. Örneğin: 0.5");
        return;
      }
      params.factor = factor; 
    }

    const formData = new FormData();
    formData.append("file", file);

    if (selectedOperation === "arithmetic" && secondFile) {
      formData.append("file2", secondFile);
    }

    const operation = operations[selectedOperation];
    if (operation.params) {
      operation.params.forEach((param) => {
        formData.append(param, params[param]);
      });
    }

    try {
      setLoading(true);
      const response = await axios.post(`http://localhost:8001${operation.url}`, formData, {
        responseType: "blob",
      });
      setResultUrl(URL.createObjectURL(response.data));
    } catch (err) {
      console.error("İşlem sırasında hata:", err);
    } finally {
      setLoading(false);
    }
  };

  const renderParams = () => {
    const op = operations[selectedOperation];
    if (!op.params) return null;
    return (
      <div className="params">
        {op.params.map((param) => (
          <div className="param-field" key={param}>
            <label>{getLabel(param)}</label>
            {renderInput(param)}
          </div>
        ))}
      </div>
    );
  };

  const getLabel = (param) => {
    const labels = {
      operation: "Histogram İşlemi",
      mode: "Renk Uzayı",
      morph_op: "Morfolojik İşlem",
      arithmetic_op: "Aritmetik İşlem",
      filter_type: "Filtre Tipi",
    };
    return labels[param] || param.toUpperCase();
  };

  const renderInput = (param) => {
    const selectOptions = {
      operation: ["stretch", "expand"],
      mode: ["hsv", "ycbcr", "lab"],
      morph_op: ["dilate", "erode", "open", "close"],
      arithmetic_op: ["subtract", "multiply"],
      filter_type: ["mean", "median"],
    };

    if (selectOptions[param]) {
      return (
        <select name={param} value={params[param] || ""} onChange={handleParamChange}>
          {selectOptions[param].map((opt) => (
            <option key={opt} value={opt}>{opt.charAt(0).toUpperCase() + opt.slice(1)}</option>
          ))}
        </select>
      );
    } else {
      return (
        <input
          type="number"
          name={param}
          value={params[param] || ""}
          onChange={handleParamChange}
          step="any"
        />
      );
    }
  };

  return (
    <div className="main-container">
      <div className="sidebar">
        <h2>DigiPicPro</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        {selectedOperation === "arithmetic" && (
          <input type="file" onChange={(e) => setSecondFile(e.target.files[0])} />
        )}
        <select value={selectedOperation} onChange={(e) => {
          setSelectedOperation(e.target.value);
          setParams(defaultParams[e.target.value] || {});
        }}>
          {Object.keys(operations).map((op) => (
            <option key={op} value={op}>{operations[op].label}</option>
          ))}
        </select>
        {renderParams()}
        <button onClick={handleSubmit}>Uygula</button>
      </div>

      <div className="content">
        {loading ? (
          <div className="spinner">İşleniyor...</div>
        ) : (
          <div className="image-display">
            {file && (
              <div className="image-card">
                <img src={URL.createObjectURL(file)} alt="Orijinal Görsel" />
              </div>
            )}
            {selectedOperation === "arithmetic" && secondFile && (
              <div className="image-card">
                <img src={URL.createObjectURL(secondFile)} alt="İkinci Görsel" />
              </div>
            )}
            {resultUrl && (
              <div className="image-card">
                <img src={resultUrl} alt="İşlenen Görsel" />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
