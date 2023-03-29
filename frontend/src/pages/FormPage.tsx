import React, {Dispatch, SetStateAction, useEffect, useState} from 'react';
import {FileUpload, FileUploadHandlerEvent} from "primereact/fileupload";
import {useMutation} from "react-query";
import {createAnalyzerTask, getAnalyzerTaskStatus} from "../services/analyzer";
import {ProgressBar} from "primereact/progressbar";
import {useDebounce} from "primereact/hooks";
import {Result} from "../types/task";

interface FormPageProps {
    setResult: Dispatch<SetStateAction<Result[]>>
}

const FormPage: React.FC<FormPageProps> = ({setResult}) => {
    const [isPending, setIsPending] = useState<boolean>(false)
    const [retryCount, debouncedRetryCount, setRetryCount] = useDebounce(0, 2000);
    const [progressBarValue, setProgressBarValue] = useState<number>(0)

    const {isSuccess: isSuccessCreated, data: taskInfo, mutate: analyzeFile} = useMutation(
        createAnalyzerTask
    );

    const {isSuccess, data: taskStatus, mutate: getTaskStatus, reset: resetStatusQuery} = useMutation(
        getAnalyzerTaskStatus
    );

    useEffect(() => {
        const interval = setInterval(() => {
            if (isPending && progressBarValue < 85) {
                setProgressBarValue(progressBarValue + 1);
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [isPending, progressBarValue])

    useEffect(() => {
        if (isSuccessCreated && taskInfo) {
            getTaskStatus(taskInfo.task_id)
        }
    }, [isSuccessCreated, getTaskStatus, taskInfo])

    useEffect(() => {
        if (isPending) {
            setRetryCount(retryCount + 1)

            if (!isSuccess || !taskStatus) {
                return
            }

            if (taskStatus.status === 'PENDING') {
                resetStatusQuery()
                getTaskStatus(taskStatus.task_id)
            }

            if (taskStatus.status === 'SUCCESS') {
                console.log(taskStatus.result)
                setProgressBarValue(100)
                setResult(taskStatus.result)
                setIsPending(false)
            }
        }
    }, [debouncedRetryCount, isPending])

    const uploadImage = async (event: FileUploadHandlerEvent) => {
        setIsPending(true);
        await analyzeFile(event.files[0])
    }

    const emptyTemplate = () => {
        return (
            <div className="flex flex-col align-items-center place-items-center">
                <i className="pi pi-image mt-3 p-5" style={{ fontSize: '5em', borderRadius: '50%', backgroundColor: 'var(--surface-b)', color: 'var(--surface-d)' }}></i>
                <span style={{ fontSize: '1.2em', color: 'var(--text-color-secondary)' }} className="my-5">
                    Перетащите сюда изображение
                </span>
            </div>
        );
    };

    return (
        <>
            {isPending && <ProgressBar value={progressBarValue}></ProgressBar>}

                    <h1 className="text-3xl font-bold p-10">Анализ таблиц на изображении</h1>

                    <FileUpload
                        name="file"
                        url={'/api/upload'}
                        accept="image/*"
                        emptyTemplate={emptyTemplate}
                        chooseLabel="Добавить файл"
                        uploadLabel="Отправить"
                        cancelLabel="Отмена"
                        disabled={isPending}
                        customUpload
                        uploadHandler={uploadImage}
                    />
        </>
    );
}

export default FormPage;