type Selects = {
    value:string,
    label:string
}

type Selected = {
    value:string,
    label:string,
    disabled:false
}

type APIRecommandation = {
    recommendations:string[],
    success:boolean,
    failed_criteria:string[],
    hasFailed:boolean
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