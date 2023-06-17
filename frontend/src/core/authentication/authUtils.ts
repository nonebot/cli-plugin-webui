import { API } from "@/api";
import { globalStore } from "@/store/app";

export async function checkTokenValidity(): Promise<boolean> {
  const api = new API();
  const token = localStorage.getItem("jwtToken");
  if (token) {
    try {
      await api.isAvailable();
    } catch (error) {
      localStorage.clear();
      return false;
    }
    globalStore().isAuthed = true;
    return true;
  }
  return false;
}
