import React, { useState } from "react";
import "./Translator.css";

const Translator = () => {
  const [inputText, setInputText] = useState(""); // <-- Fix: Define inputText
  const [translatedText, setTranslatedText] = useState("");
  const [language, setLanguage] = useState("Hindi"); // <-- Add language state

  const handleTranslate = async () => {
    if (!inputText.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText, language: language }), // <-- Include language in the request
      });

      const data = await response.json();

      if (data.translation) {
        setTranslatedText(data.translation);
      } else {
        setTranslatedText("Translation failed.");
      }
    } catch (error) {
      console.error("Error:", error);
      setTranslatedText("Error connecting to server.");
    }
  };

  return (
    <div className="translator-container">
      <h1 className="header">Multilingual Translator</h1>
      <textarea
        rows="5"
        className="input-textarea"
        placeholder="Enter English text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)} // <-- Bind inputText
      ></textarea>

      <div className="form-group">
        <label htmlFor="language-select">Select Language</label>
        <select
          id="language-select"
          className="language-select"
          value={language}
          onChange={(e) => setLanguage(e.target.value)} // <-- Add language selection
        >
          <option value="Hindi">Hindi</option>
          <option value="Bengali">Bengali</option>
        </select>
      </div>

      <button className="translate-button" onClick={handleTranslate}>
        Translate
      </button>

      <div className="output-box">
        <h2>Translated Text:</h2>
        <p className="output-text">{translatedText}</p>
      </div>
    </div>
  );
};

export default Translator;
