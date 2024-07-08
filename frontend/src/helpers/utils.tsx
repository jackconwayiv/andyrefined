import { Avatar, Flex, Text } from "@chakra-ui/react";
import dayjs from "dayjs";
import { User } from "./types";

export const isOwner = (user: User, object: any) => {
  return object.owner.email === user.email;
};

export const renderFullName = (user: User) => {
  let nameString = "";
  if (user.first_name) nameString += `${user.first_name} `;
  if (user.username) nameString += ` "${user.username}" `;
  if (user.last_name) nameString += ` ${user.last_name}`;
  return nameString;
};

export const renderSharedBy = (user: User) => {
  const renderNickname = (user: User) => {
    let nameString = "";
    if (user.first_name) nameString += `${user.first_name} `;

    if (user.last_name) nameString += `${user.last_name}`;
    if (user.username) nameString = user.username;
    return (
      <Text fontSize="10px" fontFamily={"Comic Sans MS"} alignItems="end">
        {nameString}
      </Text>
    );
  };
  const renderAvatar = (user: User) => {
    if (
      user.social_auth &&
      user.social_auth[0] &&
      user.social_auth[0].picture
    ) {
      return <Avatar mr={1} size="xs" src={user.social_auth[0].picture} />;
    }
  };

  return (
    <Flex
      direction="row"
      alignItems="center"
      justifyContent="space-between"
      p={1}
    >
      {
        <>
          <Text
            mr={1}
            fontSize="10px"
            fontFamily={"Comic Sans MS"}
            alignItems="end"
          >
            Shared by
          </Text>
          {renderAvatar(user)} {renderNickname(user)}
        </>
      }
    </Flex>
  );
};

export const renderBirthday = (dateString: string): string => {
  return dayjs(dateString).format("MMMM D");
};

export const renderAlbumDate = (dateString: string): string => {
  const date = new Date(dateString);
  const options: Intl.DateTimeFormatOptions = {
    month: "long",
    year: "numeric",
  };
  const monthYear = date.toLocaleDateString("en-US", options);
  return monthYear;
};

export function getNextBirthday(dateString: string): number {
  const today = dayjs();
  const [, month, day] = dateString.split("-").map(Number);

  let birthDate = dayjs()
    .month(month - 1)
    .date(day)
    .year(today.year());

  if (birthDate.isBefore(today, "day")) {
    birthDate = birthDate.add(1, "year");
  }

  return birthDate.valueOf();
}

export function isBirthday(user: User): boolean {
  const today = dayjs();
  const { date_of_birth } = user;

  if (!date_of_birth) {
    return false;
  }

  const [, month, day] = date_of_birth.split("-").map(Number);
  const birthDateThisYear = dayjs()
    .month(month - 1)
    .date(day)
    .year(today.year());

  const daysUntilBirthday = birthDateThisYear.diff(today, "day");
  const daysAfterBirthday = today.diff(birthDateThisYear, "day");

  if (
    (daysUntilBirthday >= 0 && daysUntilBirthday <= 6) ||
    (daysAfterBirthday >= 0 && daysAfterBirthday <= 2)
  ) {
    return true;
  }

  return false;
}
