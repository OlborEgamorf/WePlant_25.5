type Selects = {
    value:string,
    label:string
}

type Selected = {
    value:string,
    label:string,
    disabled:false
}

type Plant = {
    Name: string;
    Desc: string;
    SunNeeds: string;
    WaterNeeds: string;
    Maintenance: string;
    "Type de Sol": string;
    saison: string;
    plant_categories: string;
    min_height_cm: number;
    max_height_cm: number;
}

type APIRecommandation = {
    prediction:number
    recommendations: Plant[];
    success: boolean;
    failed_criteria: string[];
    hasFailed: boolean;
}

type APIStress = {
    prediction:number,
    prob0:number,
    prob1:number,
    prob2:number
}

type APIPredict = {
    prediction:number
}