import { Avatar, Flex, Heading, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchUserById } from "../api/user";
import { FriendType } from "../helpers/types";

const Friend = () => {
  const { id } = useParams();
  const [friend, setFriend] = useState<FriendType>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown | null>(null);

  useEffect(() => {
    const getFriend = async () => {
      try {
        const data = await fetchUserById(id || "");
        setFriend(data);
        setLoading(false);
      } catch (error) {
        setError(error);
        setLoading(false);
      }
    };

    getFriend();
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error fetching user: {JSON.stringify(error)}</div>;
  }

  return (
    <div>
      {friend ? (
        <Flex direction="column">
          <Flex>
            {friend.social_auth[0] && (
              <Avatar
                name={friend.username}
                referrerPolicy="no-referrer"
                src={friend.social_auth[0].picture}
                margin={5}
              />
            )}
            {friend.username ? (
              <Heading margin={5}>{friend.username}</Heading>
            ) : (
              <Heading margin={5}>
                {friend.first_name} {friend.last_name}
              </Heading>
            )}
          </Flex>

          {friend.date_of_birth && (
            <Text margin={5}>Birthday: {friend.date_of_birth}</Text>
          )}
          <Text margin={5}>Email: {friend.email}</Text>
        </Flex>
      ) : (
        <div>User not found</div>
      )}
    </div>
  );
};

export default Friend;
