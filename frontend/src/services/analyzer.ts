import axios, {AxiosResponse} from "axios";
import {Task} from "../types/task";


const BASE_URL = 'http://127.0.0.1:5000/api/analyzer'

export async function createAnalyzerTask(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    const response: AxiosResponse<Task> = await axios.post(`${BASE_URL}/tasks`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    return response.data;
}

export async function getAnalyzerTaskStatus(task_id: string) {
    const response: AxiosResponse<Task> = await axios.get(`${BASE_URL}/tasks/${task_id}`);
    return response.data;
}

export function generateImageURL(image: string) {
    return`${BASE_URL}/tasks/result_image?file_name=${image}`
}