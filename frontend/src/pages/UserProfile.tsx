import { Avatar, Flex, Heading } from "@chakra-ui/react";
import { AxiosError } from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchUserById } from "../api/users";
import { Friend, User } from "../helpers/types";
import {
  isBirthday,
  renderFullBirthday,
  renderFullName,
} from "../helpers/utils";

interface UserProfileProps {
  user: User;
}

const UserProfile = ({ user }: UserProfileProps) => {
  const { id } = useParams<{ id?: string }>();
  const userId = id || user.id;
  const [friend, setFriend] = useState<Friend>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown | null | AxiosError>(null);

  useEffect(() => {
    const getFriend = async () => {
      const data = await fetchUserById(userId as string);
      if (data) {
        setFriend(data);
        setLoading(false);
      } else {
        setError(error);
        setLoading(false);
      }
    };

    getFriend();
  }, [id, user]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    // if (error.response.status === 404) {
    //   return <div>User not found</div>;
    // }
    return <div>Error fetching user: {JSON.stringify(error)}</div>;
  }
  if (friend)
    return (
      <Flex direction="column" width="100%" p={2} m={2}>
        <Avatar
          name={friend.username}
          referrerPolicy="no-referrer"
          src={
            friend.social_auth && friend.social_auth[0]
              ? friend.social_auth[0].picture
              : "/avatar.jpg"
          }
          margin={3}
          size="xl"
        />

        <Heading fontFamily="Comic Sans MS" m={3}>
          {renderFullName(friend)}
        </Heading>
        <Flex alignItems="center" m={3}>
          <Heading size="md" color={isBirthday(friend) ? "orange" : "black"}>
            🎂{" "}
            {renderFullBirthday(friend.date_of_birth) || "no birthday provided"}
          </Heading>
        </Flex>
        {/* <Heading size="md">{friend.email}</Heading> */}
      </Flex>
    );

  return <div>User not found</div>;
};

export default UserProfile;
