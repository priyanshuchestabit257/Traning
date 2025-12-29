export default function TablesPage() {
  const authors = [
    {
      name: "Esthera Jackson",
      email: "esthera@simmple.com",
      role: "Manager",
      department: "Organization",
      status: "Online",
      date: "14/06/21",
      image: "/image.png",
    },
    {
      name: "Alexa Liras",
      email: "alexa@simmple.com",
      role: "Programmer",
      department: "Developer",
      status: "Offline",
      date: "14/06/21",
      image: "/image.png",
    },
    {
      name: "Laurent Michael",
      email: "laurent@simmple.com",
      role: "Executive",
      department: "Projects",
      status: "Online",
      date: "14/06/21",
      image: "/image.png",
    },
    {
      name: "Freduardo Hill",
      email: "freduardo@simmple.com",
      role: "Manager",
      department: "Organization",
      status: "Online",
      date: "14/06/21",
      image: "/image.png",
    },
    {
      name: "Daniel Thomas",
      email: "daniel@simmple.com",
      role: "Programmer",
      department: "Developer",
      status: "Offline",
      date: "14/06/21",
      image: "/image.png",
    },
    {
      name: "Mark Wilson",
      email: "mark@simmple.com",
      role: "Designer",
      department: "UI/UX Design",
      status: "Offline",
      date: "14/06/21",
      image: "/image.png",
    },
  ];

  return (
    <div className="p-6">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-xl font-bold text-gray-800">Tables</h1>
        <p className="text-sm text-gray-500">Authors Table</p>
      </div>

      {/* Table Card */}
      <div className="overflow-x-auto rounded-xl bg-white shadow-sm border">
        <table className="w-full text-sm">
          <thead className="border-b bg-gray-50">
            <tr className="text-left text-xs font-semibold text-gray-500">
              <th className="px-6 py-4">AUTHOR</th>
              <th className="px-6 py-4">FUNCTION</th>
              <th className="px-6 py-4">STATUS</th>
              <th className="px-6 py-4">EMPLOYED</th>
              <th className="px-6 py-4"></th>
            </tr>
          </thead>

          <tbody>
            {authors.map((author, index) => (
              <tr key={index} className="border-b last:border-b-0">
                {/* Author */}
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <img
                      src={author.image}
                      alt={author.name}
                      className="h-10 w-10 rounded-full object-cover"
                    />
                    <div>
                      <p className="font-semibold text-gray-800">
                        {author.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        {author.email}
                      </p>
                    </div>
                  </div>
                </td>

                {/* Function */}
                <td className="px-6 py-4">
                  <p className="font-semibold text-gray-800">
                    {author.role}
                  </p>
                  <p className="text-xs text-gray-500">
                    {author.department}
                  </p>
                </td>

                {/* Status */}
                <td className="px-6 py-4">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      author.status === "Online"
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-200 text-gray-600"
                    }`}
                  >
                    {author.status}
                  </span>
                </td>

                {/* Employed */}
                <td className="px-6 py-4 text-gray-800 font-medium">
                  {author.date}
                </td>

                {/* Action */}
                <td className="px-6 py-4 text-sm font-medium text-blue-600 hover:underline cursor-pointer">
                  Edit
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
