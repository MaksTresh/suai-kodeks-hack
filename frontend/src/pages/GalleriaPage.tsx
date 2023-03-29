import React from 'react';
import {Result} from "../types/task";
import {generateImageURL} from "../services/analyzer";
import {Card} from "primereact/card";
import {Image} from "primereact/image";

interface GalleriaPageProps {
    result: Result[]
}

const GalleriaPage: React.FC<GalleriaPageProps> = ({result}) => {
    return (
        <>
            {result.map(item => (
                <Card title={`Тип: ${item.type}`} className="rounded mb-4">
                    <Image src={generateImageURL(item.table_img)} width="400" preview />
                </Card>
            ))}
        </>
    )
}

export default GalleriaPage;