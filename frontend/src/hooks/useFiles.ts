import { useState, useEffect, useCallback } from "react";
import * as filesAPI from "../api/files";
import { FileEntry } from "../types/files";

export function useFiles(initialPath: string = "Home") {
  const [files, setFiles] = useState<FileEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async (path = initialPath) => {
    setLoading(true);
    setError(null);
    try {
      const fileList = await filesAPI.listFiles(path);
      setFiles(fileList);
    } catch (e: any) {
      setError(e.message || "Failed to load files.");
    }
    setLoading(false);
  }, [initialPath]);

  useEffect(() => {
    refresh(initialPath);
  }, [refresh, initialPath]);

  return { files, loading, error, refresh };
}
