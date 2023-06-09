import React from "react";
import { Link } from "react-router-dom";

const CourseCard = ({ course, user }) => {
  return (
    <div>
      {course ? (
        <Link
          to={`/courses/${course?.coursename}/${course["_id"]}`}
          state={user}
          className="mx-auto block w-[90%] rounded-lg border border-gray-200 bg-white p-6 shadow hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700 md:w-full"
        >
          <h5
            title={course?.coursename.replace(/-/g, " ")}
            className="mb-2 h-16 text-center text-2xl font-bold tracking-tight text-gray-900 line-clamp-2 dark:text-white md:h-24 md:text-start md:line-clamp-3"
          >
            {course.coursename.replace(/-/g, " ")}
          </h5>
          <p
            title={course?.objective}
            className="h-24 text-center font-normal text-gray-700 line-clamp-4 dark:text-gray-400 md:h-36 md:text-start md:line-clamp-6"
          >
            {course?.objective}
          </p>
          <div className="mt-4 flex items-center justify-evenly text-gray-900 dark:text-white md:justify-between">
            <span className="text-lg font-bold text-blue-700 dark:text-blue-600">
              ${course?.fees}
            </span>
          </div>
        </Link>
      ) : (
        ""
      )}
    </div>
  );
};

export default CourseCard;
