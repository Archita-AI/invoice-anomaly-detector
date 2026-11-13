import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState("csv");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setFile(selectedFile);
    setResult(null);
    setError("");
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    const expectedExtension = fileType === "pdf" ? ".pdf" : ".csv";

    if (!file.name.toLowerCase().endsWith(expectedExtension)) {
      setError(`Please select a ${fileType.toUpperCase()} file.`);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    const endpoint =
      fileType === "pdf"
        ? `${API_URL}/analyze`
        : `${API_URL}/analyze-csv`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the backend. Please check whether the server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!result?.results) return;

    const rows = result.results;

    if (!rows.length) return;

    const headers = Object.keys(rows[0]);

    const escapeCSV = (value) => {
      const text =
        value === null || value === undefined ? "" : String(value);

      return `"${text.replace(/"/g, '""')}"`;
    };

    const csvContent = [
      headers.map(escapeCSV).join(","),
      ...rows.map((row) =>
        headers.map((header) => escapeCSV(row[header])).join(",")
      ),
    ].join("\n");

    const blob = new Blob([csvContent], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "invoice_analysis_results.csv";
    link.click();

    URL.revokeObjectURL(url);
  };

  const csvSummary = result?.summary;

  const analysis = result?.analysis;

  const isAnomaly = (value) =>
    String(value).toLowerCase() === "anomaly" ||
    String(value) === "-1";

  return (
    <div className="app">
      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">
          <div className="logo-icon">✦</div>
          <span>
            Invoice<span className="highlight">Guard</span>
          </span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#analyze">Analyse</a>
          <a href="#about">About</a>
        </div>

        <a href="#analyze" className="nav-button">
          Get Started ↗
        </a>
      </nav>

      {/* Hero */}
      <section className="hero" id="home">
        <div className="hero-content">
          <div className="tag">
            <span className="pulse"></span>
            INTELLIGENT INVOICE ANALYSIS
          </div>

          <h1>
            Detect the unusual.
            <br />
            <span>Protect your business.</span>
          </h1>

          <p>
            An intelligent invoice anomaly detection platform designed
            to identify unusual transactions, analyse vendor behaviour
            and help businesses make smarter financial decisions.
          </p>

          <div className="hero-buttons">
            <a href="#analyze" className="primary-button">
              Analyse an Invoice ↗
            </a>

            <a href="#features" className="secondary-button">
              Explore Features →
            </a>
          </div>

          <div className="hero-note">
            <span>✓</span> Machine Learning Powered
            <span>✓</span> Vendor-Based Analysis
          </div>
        </div>

        {/* Preview */}
        <div className="preview-card">
          <div className="preview-header">
            <div>
              <span className="preview-label">PLATFORM OVERVIEW</span>
              <h3>InvoiceGuard</h3>
            </div>
            <span className="live-badge">● ML POWERED</span>
          </div>

          <div className="preview-stats">
            <div className="stat-box">
              <span>Input Formats</span>
              <h2>02</h2>
              <small>PDF and CSV</small>
            </div>

            <div className="stat-box">
              <span>Detection</span>
              <h2 className="red">AI</h2>
              <small>Isolation Forest</small>
            </div>
          </div>

          <div className="preview-analysis">
            <div className="analysis-title">
              <span>Analysis capabilities</span>
              <span>Available</span>
            </div>

            <div className="invoice-row">
              <div className="invoice-icon">PDF</div>
              <div className="invoice-info">
                <strong>Individual invoices</strong>
                <small>PDF extraction and analysis</small>
              </div>
              <span className="status normal">Ready</span>
            </div>

            <div className="invoice-row">
              <div className="invoice-icon">CSV</div>
              <div className="invoice-info">
                <strong>Bulk analysis</strong>
                <small>Multiple invoice detection</small>
              </div>
              <span className="status normal">Ready</span>
            </div>
          </div>

          <div className="preview-footer">
            Powered by Machine Learning
            <span>✦</span>
          </div>
        </div>
      </section>

      {/* Upload Section */}
      <section className="analyze-section" id="analyze">
        <div className="section-heading">
          <span>GET STARTED</span>
          <h2>Analyse your invoices.</h2>
          <p>
            Upload an invoice PDF or a CSV dataset to detect unusual
            transaction patterns.
          </p>
        </div>

        <div className="upload-card">
          <div className="upload-tabs">
            <button
              className={fileType === "csv" ? "active" : ""}
              onClick={() => {
                setFileType("csv");
                setFile(null);
                setResult(null);
                setError("");
              }}
            >
              CSV Dataset
            </button>

            <button
              className={fileType === "pdf" ? "active" : ""}
              onClick={() => {
                setFileType("pdf");
                setFile(null);
                setResult(null);
                setError("");
              }}
            >
              PDF Invoice
            </button>
          </div>

          <div className="upload-area">
            <div className="upload-symbol">
              {fileType === "csv" ? "▤" : "▧"}
            </div>

            <h3>
              Upload your {fileType.toUpperCase()} file
            </h3>

            <p>
              {fileType === "csv"
                ? "Upload a CSV containing invoice records."
                : "Upload a PDF invoice for individual analysis."}
            </p>

            <label className="choose-file">
              Choose File
              <input
                type="file"
                accept={fileType === "csv" ? ".csv" : ".pdf"}
                onChange={handleFileChange}
              />
            </label>

            {file && (
              <div className="selected-file">
                ✓ Selected: {file.name}
              </div>
            )}
          </div>

          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analysing..." : "Run Anomaly Detection ↗"}
          </button>

          {loading && (
            <p className="loading-message">
              Your invoice data is being processed by the ML model.
              Please wait...
            </p>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>

        {/* Results */}
        {result && (
          <div className="results-section">
            <div className="results-heading">
              <div>
                <span>ANALYSIS COMPLETE</span>
                <h2>Detection Results</h2>
                <p>{result.filename}</p>
              </div>

              {result.results && (
                <button
                  className="download-button"
                  onClick={downloadCSV}
                >
                  ↓ Download CSV
                </button>
              )}
            </div>

            {csvSummary && (
              <>
                <div className="results-stats">
                  <div className="result-stat">
                    <span>Total Invoices</span>
                    <h2>{csvSummary.total_invoices}</h2>
                  </div>

                  <div className="result-stat">
                    <span>Normal Invoices</span>
                    <h2>{csvSummary.normal_invoices}</h2>
                  </div>

                  <div className="result-stat">
                    <span>Anomalies Detected</span>
                    <h2 className="red">
                      {csvSummary.anomaly_invoices}
                    </h2>
                  </div>
                </div>

                <div className="table-wrapper">
                  <h3>Invoice Analysis</h3>

                  <table>
                    <thead>
                      <tr>
                        <th>Invoice ID</th>
                        <th>Vendor</th>
                        <th>Amount</th>
                        <th>Anomaly Score</th>
                        <th>Prediction</th>
                      </tr>
                    </thead>

                    <tbody>
                      {result.results.map((row, index) => (
                        <tr key={index}>
                          <td>{row.invoice_id ?? "-"}</td>
                          <td>{row.vendor ?? "-"}</td>
                          <td>
                            {row.amount !== null &&
                            row.amount !== undefined
                              ? Number(row.amount).toLocaleString("en-IN")
                              : "-"}
                          </td>
                          <td>
                            {row.anomaly_score !== null &&
                            row.anomaly_score !== undefined
                              ? Number(row.anomaly_score).toFixed(4)
                              : "-"}
                          </td>
                          <td>
                            <span
                              className={`status ${
                                isAnomaly(row.model_result)
                                  ? "anomaly"
                                  : "normal"
                              }`}
                            >
                              {row.model_result ?? "-"}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}

            {analysis && (
              <div className="pdf-result">
                <h3>Individual Invoice Analysis</h3>

                <div className="pdf-result-grid">
                  {Object.entries(analysis).map(([key, value]) => (
                    <div className="pdf-result-item" key={key}>
                      <span>
                        {key.replace(/_/g, " ")}
                      </span>
                      <strong>
                        {value === null
                          ? "Not available"
                          : typeof value === "object"
                            ? JSON.stringify(value)
                            : String(value)}
                      </strong>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <p className="disclaimer">
              Anomaly detection identifies unusual patterns, not
              confirmed fraud. Flagged invoices should be reviewed
              by a human.
            </p>
          </div>
        )}
      </section>

      {/* Features */}
      <section className="features" id="features">
        <div className="section-heading">
          <span>WHAT WE OFFER</span>
          <h2>Smarter invoice intelligence.</h2>
          <p>
            Everything you need to identify unusual invoice activity.
          </p>
        </div>

        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">⌕</div>
            <h3>Anomaly Detection</h3>
            <p>
              Identify unusual invoice transactions using the
              Isolation Forest machine learning algorithm.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">◈</div>
            <h3>Vendor Analysis</h3>
            <p>
              Analyse vendor transaction patterns and identify
              unexpected changes.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">↗</div>
            <h3>Risk Assessment</h3>
            <p>
              Review anomaly scores and prioritise suspicious
              transactions for further investigation.
            </p>
          </div>
        </div>
      </section>

      {/* About */}
      <section className="about" id="about">
        <div>
          <span>ABOUT THE PROJECT</span>
          <h2>Making financial analysis more intelligent.</h2>
        </div>

        <p>
          InvoiceGuard is a machine learning-based project that helps
          small businesses identify unusual invoice patterns and
          prioritise transactions for human review.
        </p>
      </section>

      <footer>
        <div className="logo">
          <div className="logo-icon">✦</div>
          <span>
            Invoice<span className="highlight">Guard</span>
          </span>
        </div>

        <p>
          Intelligent invoice analysis for smarter businesses.
        </p>

        <small>© 2026 InvoiceGuard. Academic Project.</small>
      </footer>
    </div>
  );
}

export default App;