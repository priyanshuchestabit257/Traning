import { ArrowLeft } from "lucide-react";

export default function ProfilePage() {
  // Static mock data
  const userData = {
    name: "Nina Valentine",
    jobTitle: "Actress",
    email: "nina_val@example.com",
    linkedIn: "linkedin.com",
    twitter: "www.x.com",
    facebook: "facebook.com",
    bio: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent aliquet odio augue, in dapibus lacus imperdiet ut. Quisque elementum placerat neque rhoncus tempus. Cras id suscipit diam, sit amet rutrum ipsum. Vestibulum rutrum elit lacinia sapien porta pulvinar.",
    
  };

  return (
    <div className="min-h-screen bg-white p-8 font-sans text-gray-800">
      <div className="mx-auto max-w-5xl">

        
        <a
          href="/dashboard"
          className="mb-6 inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:underline"
        ><ArrowLeft className="h-4 w-4" />
          Go back
        </a>

       
        <div className="overflow-hidden border border-gray-200 bg-white">

          {/* Top Section */}
          <div className="flex flex-col md:flex-row">

            {/* Profile Image */}
            <div className="relative h-64 w-full md:h-auto md:w-72 shrink-0">
              <img
  src="/image.png"
  alt="Profile"
  className="h-full w-full object-cover p-6"
/>

            </div>

            {/* Info Columns */}
            <div className="flex grow flex-col md:flex-row">

              {/* Left Column */}
              <div className="flex-1 border-t border-gray-200 md:border-l md:border-t-0 md:border-r">
                <InfoRow label="Name" value={userData.name} />
                <InfoRow label="Job Title" value={userData.jobTitle} />
                <InfoRow label="Email" value={userData.email} isLink />
              </div>

              {/* Right Column */}
              <div className="flex-1 border-t border-gray-200 md:border-t-0">
                <InfoRow label="LinkedIn" value={userData.linkedIn} isLink />
                <InfoRow label="Twitter" value={userData.twitter} isLink />
                <InfoRow label="Facebook" value={userData.facebook} isLink />
              </div>

            </div>
          </div>

          {/* Bio */}
          <div className="border-t border-gray-200 p-6">
            <h3 className="mb-2 text-sm text-gray-500">Bio</h3>
            <p className="leading-relaxed text-gray-600">
              {userData.bio}
            </p>
          </div>

          {/* Footer */}
          <div className="border-t border-gray-100 bg-gray-50/30 p-6">
            <button className="text-sm font-medium text-blue-600 hover:underline">
              Edit Profile
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}

/* Helper Component */
function InfoRow({ label, value, isLink = false }) {
  return (
    <div className="border-b border-gray-100 p-4 last:border-b-0 md:p-6">
      <dt className="mb-1 text-xs text-gray-400">{label}</dt>
      <dd
        className={`text-sm font-medium ${
          isLink
            ? "cursor-pointer text-blue-600 hover:underline"
            : "text-gray-700"
        }`}
      >
        {value}
      </dd>
    </div>
  );
}
