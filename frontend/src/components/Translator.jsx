import React, { useState, useEffect } from "react";
import "./Translator.css";

const Translator = () => {
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [inputLanguage, setInputLanguage] = useState("English");
  const [outputLanguage, setOutputLanguage] = useState("Hindi");
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    document.body.className = isDarkMode ? "dark-mode" : "light-mode";
  }, [isDarkMode]);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: inputText,
          source_lang: inputLanguage,
          target_lang: outputLanguage,
        }),
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

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className="translator-page">
      <div className="translator-container">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-title-container">
            <h1 className="sidebar-title">🌍 MULTILINGUAL TRANSLATION</h1>
            <hr className="sidebar-divider" />
            <h2 className="sidebar-subtitle">भाषा अनुवाद</h2>
          </div>
        </div>

        {/* Main Content */}
        <div className="main-content">
          {/* Toggle Button */}
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            title="Toggle Theme"
          >
            {isDarkMode ? "☀️" : "🌙"}
          </button>

          <h2 className="header" style={{ marginTop: "0", paddingTop: "10px" }}>
            Language Translation
          </h2>

          <textarea
            rows="5"
            className="input-textarea"
            placeholder="Enter text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          ></textarea>

          <div className="form-group">
            <label htmlFor="input-language-select">Input Language:</label>
            <select
              id="input-language-select"
              className="language-select"
              value={inputLanguage}
              onChange={(e) => setInputLanguage(e.target.value)}
            >
              <option value="English">English</option>
              <option value="Hindi">Hindi</option>
              <option value="Bengali">Bengali</option>
              <option value="Marathi">Marathi</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="output-language-select">Output Language:</label>
            <select
              id="output-language-select"
              className="language-select"
              value={outputLanguage}
              onChange={(e) => setOutputLanguage(e.target.value)}
            >
              <option value="Hindi">Hindi</option>
              <option value="Bengali">Bengali</option>
              <option value="Marathi">Marathi</option>
              <option value="English">English</option>
            </select>
          </div>

          <button className="translate-button" onClick={handleTranslate}>
            🔄 Translate
          </button>

          <div className="output-box">
            <h2>Translated Text:</h2>
            <p className="output-text">{translatedText}</p>
          </div>
        </div>
      </div>

      {/* Sticky-like footer */}
      <footer className="app-footer">
        <p>
          © {new Date().getFullYear()} Multilingual Translator. All rights
          reserved.
        </p>
      </footer>
    </div>
  );
};

export default Translator;
