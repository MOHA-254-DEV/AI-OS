import React from "react";
import { useOrganization } from "../../context/OrganizationContext";
import { formatDateTime } from "../../utils/helpers";

const Organizations: React.FC = () => {
  const { organizations } = useOrganization();
  return (
    <div>
      <h2>Organizations</h2>
      <ul>
        {organizations.map((org) => (
          <li key={org.id}>
            <b>{org.name}</b> (Created: {formatDateTime(org.createdAt)})
          </li>
        ))}
      </ul>
    </div>
  );
};
export default Organizations;
