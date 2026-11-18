import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class GlobalErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-cream flex flex-col items-center justify-center p-4">
          <div className="bg-surface p-8 rounded-sm shadow-sm max-w-2xl w-full text-center border border-border">
            <h2 className="text-2xl font-heading text-forest mb-4">Something went wrong while loading this page.</h2>
            <p className="text-stone mb-6 text-sm">
              An unexpected error occurred. You can try reloading the view.
            </p>
            {import.meta.env.DEV && this.state.error && (
              <div className="mb-6 p-4 bg-terracotta/10 border border-terracotta/20 rounded text-left overflow-auto max-h-64 text-xs font-mono text-terracotta">
                <p className="font-bold mb-2">{this.state.error.message}</p>
                <pre>{this.state.error.stack}</pre>
              </div>
            )}
            <button
              onClick={this.handleRetry}
              className="bg-forest text-cream px-6 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

