// @ts-ignore
import drexelJSON from "./drexel.json" assert { type: "json" };

export type SinglePrerequisite = {
    codeName: string;
    minimumGrade: string;
};

export type Prerequisite = SinglePrerequisite | PrerequisiteOption | string;

export type PrerequisiteOption = {
    oneOf: Prerequisite[];
};

export type Course = {
    codeName: string;
    properName: string;
    credits: number;
    majorName: string;
    prerequisites: Prerequisite[];
};

export type Major = {
    name: string;
    courses: Course[];
    collegeName: string;
};

export type College = {
    name: string;
    majors: Major[];
};

export type Drexel = {
    colleges: College[];
};

const drexel = drexelJSON as Drexel;

/**
 * Returns the first course that satisfies the given properties.
 * 
 * **Parameters**
 * ```ts
 * let properties: Partial<Course>
 * ```
 * - The properties the course must have
 *
 * **Returns**
 * 
 * The course that satsfies the given properties.
 */
export function courseWith(properties: Partial<Course>): Course | null {
    let correctCourse: Course | null = null;
    drexel.colleges.some(college => {
        return college.majors.some(major => {
            return major.courses.some(course => {
                if ((Object.keys(properties) as (keyof Course)[]).filter(property => properties[property]).every(property => {
                    return course[property] === properties[property];
                })) {
                    correctCourse = course;
                    return true;
                }
                return false;
            });
        });
    });

    return correctCourse;
}

/**
 * Returns the first major that satisfies the given properties.
 * 
 * **Parameters**
 * ```ts
 * let properties: Partial<Major>
 * ```
 * - The properties the major must have
 *
 * **Returns**
 * 
 * The major that satsfies the given properties.
 */
export function majorWith(properties: Partial<Major>): Major | null {
    let correctMajor: Major | null = null;
    drexel.colleges.some(college => {
        return college.majors.some(major => {
            if ((Object.keys(properties) as (keyof Major)[]).filter(property => properties[property]).every(property => {
                return major[property] === properties[property];
            })) {
                correctMajor = major;
                return true;
            }
            return false;
        });
    });

    return correctMajor;
}

/**
 * Returns the first college that satisfies the given properties.
 * 
 * **Parameters**
 * ```ts
 * let properties: Partial<College>
 * ```
 * - The properties the college must have
 *
 * **Returns**
 * 
 * The college that satsfies the given properties.
 */
export function collegeWith(properties: Partial<College>): College | null {
    let correctCollege: College | null = null;
    drexel.colleges.some(college => {
        if ((Object.keys(properties) as (keyof College)[]).filter(property => properties[property]).every(property => {
            return college[property] === properties[property];
        })) {
            correctCollege = college;
            return true;
        }
        return false;
    });

    return correctCollege;
}

/**
 * Returns whether or not the given courses are enough to satisfy the prerequisites for the given course. This
 * returns only whether the given courses are sufficient, and cannot determine if they are minimally necessary.
 * 
 * **Parameters**
 * ```ts
 * let course: Course
 * ```
 * - The course to check if it can be taken.
 * ```ts
 * let courses: Course[]
 * ```
 * - The completed courses which may or may not suffice to take the previous course.
 *
 * **Returns**
 * 
 * `true` if the given courses are enough to satisfy the prerequisites of the given course, `false` otherwise. 
 */
export function canTake(course: Course, courses: Course[]): boolean {
    return course.prerequisites.every(prerequisite => prerequisiteIsSatisfied(prerequisite, courses));
}

/**
 * Returns whether or not the given prerequisite object is satsified by the given courses.
 * 
 * **Parameters**
 * ```ts
 * let prerequisite: Prerequisite
 * ```
 * - The prerequisite object to check
 * ```ts
 * let courses: Course[]
 * ```
 * - The courses to check if satisfy the prerequisite
 * 
 * **Returns**
 * 
 * `true` if the prerequisite is satsified from passing the given courses, `false` otherwise.
 */
export function prerequisiteIsSatisfied(prerequisite: Prerequisite, courses: Course[]): boolean {
    if (typeof prerequisite === "string") return true;
    if ("codeName" in prerequisite) return courses.some(course => prerequisite.codeName === course.codeName);
    return prerequisite.oneOf.some(course => prerequisiteIsSatisfied(course, courses));
}

/**
 * Returns the prerequisite that is missing in order to satisfy the given course, or `[]` if all prerequisites
 * are satisfied by the given courses.
 * 
 * **Parameters**
 * ```ts
 * let course: Course
 * ```
 * - The course to check the prerequisites of
 * ```ts
 * let courses: Course[]
 * ```
 * - The completed courses that may or may not satisfy the prerequisites
 * 
 * **Returns**
 * 
 * the prerequisites that are yet to be fulfilled by the given courses.
 */
export function missingPrerequisites(course: Course, courses: Course[]): Prerequisite[] {
    let prerequisites: Prerequisite[] = [];
    course.prerequisites.forEach(prerequisite => {
        if (typeof prerequisite === "string") return;
        if ("codeName" in prerequisite) {
            if (!courses.map(course => course.codeName).includes(prerequisite.codeName)) prerequisites.push(prerequisite);
            return;
        }
        if (!prerequisiteIsSatisfied(prerequisite, courses)) prerequisites.push(prerequisite);
    });

    return prerequisites;
}
