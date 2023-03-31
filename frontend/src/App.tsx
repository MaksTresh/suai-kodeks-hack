import React, {useState} from 'react';
import FormPage from "./pages/FormPage";
import {Result} from "./types/task";
import GalleriaPage from "./pages/GalleriaPage";

function App() {
    const [result, setResult] = useState<Result[]>([]);

    return (
    <div className="App">
        <div className="grid h-screen place-items-center w-100%">
            <div className={`min-[600px]:p-10 ${result.length === 0 ? "bg-white max rounded border" : ""}`}>
                {result.length === 0 ? <FormPage setResult={setResult} /> : <GalleriaPage result={result} />}
            </div>
        </div>
    </div>
    );
}

export default App;
