export interface Result {
    table_img: string;
    type: string;
}

export interface Task {
    task_id: string;
    status: string;
    result: Result[];
}