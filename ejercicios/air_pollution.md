Air Pollution
================

Este ejercicio forma parte del curso *R Programming*, dictado por la Universidad de Johns Hopkins en [Coursera](https://www.coursera.org/learn/r-programming).

**Consigna.** El ejercicio está dividido en tres partes. En la *Parte I* hay que escribir una función para calcular la media del nivel de contaminante (sulfato o nitrato) en el aire para una o varias estaciones de monitoreo. En la *Parte II*, escribir una función que informe el número de casos observados (no NA) para uno o más archivos CSV. Por último, en la *Parte III*, hacer una función para calcular la correlación entre los niveles de sulfato y nitrato en el aire.

**Data.** El dataset se encuentra en un archivo zip, "specdata.zip". Este archivo zip contiene 332 archivos CSV, en lo cuales se encuentran los datos de monitoreo de contaminación del aire por partículas finas (PM) de sulfato o nitrato en 332 ubicaciones en los Estados Unidos. Cada archivo contiene datos de un solo monitor. Las variables, para todos los archivos, son:

-   date: fecha de la observación en formato AAAA-MM-DD (año-mes-día).

-   sulfate: nivel de PM de sulfato en el aire en esa fecha (medido en microgramos por metro cúbico).

-   nitrate: nivel de PM de nitrato en el aire en esa fecha (medido en microgramos por metro cúbico).

### Parte 1 - Pollution Mean

``` r
pollutantmean <- function(directory, pollutant, id = 1:332){
    # "directory": carpeta que contiene los archivos csv.
    # "pollutant": contaminante (sulfate o nitrate).
    # "id": número de la estación de monitoreo. Puede pasarse como
    # parámetro un único valor, un vector o un rango de valores.
    
    # Crea una lista que contiene los nombres de los archivos CSV 
    # que se encuentran en "directory"
    file_list <- list.files(path = directory, 
                            pattern = ".csv", 
                            full.names = TRUE)                 
    
    # Crea un vector de datos numéricos
    values <- numeric()
    
    for (i in id){
        # Lee cada archivo CSV, y 
        data <- read.csv(file_list[i])
        # guarda los datos del "pollutant" en "values"
        values <- c(values, data[[pollutant]])
    }
    
    # Calcula el promedio
    return(mean(values, na.rm = TRUE))
}
```

``` r
pollutantmean("specdata", "nitrate", 23)
```

    ## [1] 1.280833

``` r
pollutantmean("specdata", "nitrate", c(2, 34, 68, 100))
```

    ## [1] 1.078081

``` r
pollutantmean("specdata", "sulfate", 1:10)
```

    ## [1] 4.064128

### Parte 2 - Complete Cases

``` r
complete <- function(directory, id = 1:332){
    # "directory": carpeta que contiene los archivos csv.
    # "id": número de la estación de monitoreo. Puede pasarse como
    # parámetro un único valor, un vector o un rango de valores.
    
    file_list <- list.files(path = directory, 
                            pattern = ".csv", 
                            full.names = TRUE)
    nobs <- numeric()
    for (i in id){
        # Lee cada archivo CSV, y
        data <- read.csv(file_list[i])
        # guarda la cantidad de casos observados 
        # de cada archivo en "nobs"
        nobs <- c(nobs, sum(complete.cases(data)))
    }
    return(data.frame(id, nobs))
}
```

``` r
complete("specdata", 1)
```

    ##   id nobs
    ## 1  1  117

``` r
complete("specdata", c(2, 4, 8, 10, 12))
```

    ##   id nobs
    ## 1  2 1041
    ## 2  4  474
    ## 3  8  192
    ## 4 10  148
    ## 5 12   96

``` r
complete("specdata", 30:25)
```

    ##   id nobs
    ## 1 30  932
    ## 2 29  711
    ## 3 28  475
    ## 4 27  338
    ## 5 26  586
    ## 6 25  463

### Parte 3 - Correlation

``` r
corr <- function(directory, threshold = 0){
    # "directory": carpeta que contiene los archivos csv.
    # "threshold": valor númerico que representa la cantidad
    # de valores no nulos requeridos para calcular la correlación.
    
    file_list <- list.files(path = directory, 
                            pattern = ".csv",
                            full.names = TRUE)
    
    # Crea un DataFrame con el número de observaciones completas
    # (no NA) por cada archivo CSV. LLama a la funcion "complete"
    df <- complete(directory)
    
    # Extrae los ids que tengan los nobs mayores a "threshold"
    id_mayores <- df[df["nobs"] > threshold, ]$id
    
    correlation <- numeric()
    
    for (id in id_mayores){
        # Lee cada archivo CSV, y 
        data <- read.csv(file_list[id])
        # extrae los valores completos, y
        cases <- data[complete.cases(data), ]
        # calcula la correlación entre sulfate y nitrate para cada id
        correlation <- c(correlation, cor(cases$sulfate, cases$nitrate))
    }
    return(data.frame(id_mayores, correlation))
}                       
```

``` r
cr <- corr("specdata", 150)
head(cr)
```

    ##   id_mayores correlation
    ## 1          2 -0.01895754
    ## 2          3 -0.14051254
    ## 3          4 -0.04389737
    ## 4          5 -0.06815956
    ## 5          6 -0.12350667
    ## 6          7 -0.07588814
