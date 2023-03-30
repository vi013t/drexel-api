# drexel-api

`drexel-api` is a node module providing a public API for all things related to drexel including colleges, majors, courses, faculty, and student organizations.

## Installation
```bash
npm i drexel
```

## Usage
The API provides several helper functions for accessing Drexel's data:

```ts
import * as drexel from "drexel";

let programming1 = drexel.courseWith({ codeName: "CS-171" });
console.log(programming1.credits);

let csMajor = drexel.majorWith({ name: programming1.majorName });
console.log(csMajor.courses);
```

For a full list of functions, see the docs. 

## Privacy
The data provided does give certain information about faculty, sometimes including phone numbers and emails. However, all data was retrieved from websites accessible to the general public, including those who are not Drexel students. 
