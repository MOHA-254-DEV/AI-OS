import React from "react";

interface State { hasError: boolean; error?: Error; }
export default class ErrorBoundary extends React.Component<{}, State> {
  constructor(props: {}) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Can log error to Sentry, LogRocket, etc. here
    // eslint-disable-next-line no-console
    console.error("ErrorBoundary caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: 40,
          color: "red",
          fontWeight: 700,
          background: "#fff0f0",
          borderRadius: 16,
          fontSize: 18,
        }}>
          <h2>Something went wrong!</h2>
          <p>
            An unexpected error occurred. Please refresh the page.<br />
            If the problem persists, contact your system administrator.
          </p>
          {this.state.error && (
            <pre style={{
              background: "#ffeaea",
              color: "#b71c1c",
              padding: 8,
              borderRadius: 8,
              fontSize: 14,
              marginTop: 12,
              whiteSpace: "pre-wrap",
              wordBreak: "break-all"
            }}>
              {this.state.error.message}
            </pre>
          )}
        </div>
      );
    }
    return this.props.children;
  }
}
