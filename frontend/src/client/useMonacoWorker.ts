import * as monaco from "monaco-editor/esm/vs/editor/editor.api.js";

self.MonacoEnvironment = {
  getWorkerUrl: () => {
    return "./editor.worker.bundle.js";
  },
};
