import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 60000,
});

export const fetchBooks = async () => (await apiClient.get("/books/")).data;
export const fetchBookDetail = async (id) => (await apiClient.get(`/books/${id}/`)).data;
export const fetchRecommendations = async (id) => (await apiClient.get(`/recommend/${id}/`)).data;
export const scrapeBooks = async (pages = 1) => (await apiClient.post("/upload/", { pages })).data;
export const askQuestion = async (question) => (await apiClient.post("/ask/", { question, top_k: 4 })).data;
export const fetchHistory = async () => (await apiClient.get("/history/")).data;

