import { useState } from "react";
import styles from "./App.module.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
  setLoading(true);
  setImage(null);
  try {
    const res = await fetch("http://localhost:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }), // send as an object
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
      <input
        type="text"
        placeholder="Enter your prompt (e.g., Ajrakh pattern)"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={generateImage} disabled={loading}>
        {loading ? "Generating..." : "Generate"}
      </button>
      </div>
      <br></br>
      {image && <img src={image} alt="Generated design" className={styles.result} />}
    </div>
  );
}

export default App;
