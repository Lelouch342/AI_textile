import { useState, useRef } from "react";
import styles from "./App.module.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);

  const handleInputChange = (e) => {
    const textarea = textareaRef.current;
    setPrompt(e.target.value);

    // Auto-resize behavior
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  const generateImage = async () => {
    setLoading(true);
    setImage(null);
    try {
      const res = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setImage(`data:image/png;base64,${data.image}`);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className={styles.container}>
      <h1>Textile Design Generator</h1>

      <div className={styles.form}>
        <textarea
          ref={textareaRef}
          className={styles.textarea}
          placeholder="Enter your design prompt (e.g., 'Ajrakh block print with indigo and geometric motifs')"
          value={prompt}
          onChange={handleInputChange}
          rows={1}
        />
        <button onClick={generateImage} disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>

      {image && (
        <img
          src={image}
          alt="Generated design"
          className={styles.result}
        />
      )}
    </div>
  );
}

export default App;
