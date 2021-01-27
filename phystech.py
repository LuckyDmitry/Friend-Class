from typing import Optional
from datetime import datetime
from time import gmtime, strftime


class Phystech:
    __uid = 0
    __all_users = set()
    __user_history = {}

    def __init__(
            self,
            name: str,
            login: str,
            password: str,
            graduation_year: Optional[int] = None,
            birthday: Optional[datetime] = None,
            status: Optional[str] = None,
            friends: Optional[set] = None,
    ):
        self.name = name
        self.status = status
        self.last_online = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.__uid = Phystech.__uid
        Phystech.__uid += 1

        self._birthday = birthday
        self._friends = self._initialize_friends(friends)
        self._block_users = set()
        self._incoming_friend_requests = set()
        self._outcoming_friend_requests = set()
        self._graduation_year = graduation_year
        self.__login = login
        self.__password = password

        self.__all_users.add(self)
        self.__user_history[self.__uid] = [(self.last_online, "Create an account")]

    @property
    def is_graduate(self) -> Optional[bool]:
        if self._graduation_year is not None:
            return datetime.now().year - self._graduation_year > 0
        return None

    @staticmethod
    def _initialize_friends(friends: set) -> set:
        if not friends:
            return set()
        return friends

    def _get_uid(self) -> int:
        return self.__uid

    def _update_online_status(self, action: str = None) -> None:
        """
        Update a user online status. Add to a list of actions.
        :param action: str - a user action
        :return: None
        """
        self.last_online = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        Phystech.__user_history[self.__uid].append((self.last_online, action))

    @staticmethod
    def _get_phystech_object(user_uid: int) -> 'Phystech':
        """
        Get an instance of a class Phystech
        :param user_uid: int
        :return: Phystech object
        """
        for user in Phystech.__all_users:
            if user._get_uid() == user_uid:
                return user
        raise KeyError(f'Id {user_uid} wasn\'t found!')

    def _get_name(self) -> str:
        return self.name

    @staticmethod
    def _get_user_history(user_uid):
        return Phystech.__user_history[user_uid]

    def get_block_users_list(self, flag: bool = True) -> set:
        """
        Return a set of blocked users
        :return: set
        """
        if flag:
            self._update_online_status('Get blocked users')
        return self._block_users

    def get_friends_list(self, flag: bool = True) -> set:
        """
        Return a set of user friends
        :return: set
        """
        if flag:
            self._update_online_status("Get friends")
        return self._friends

    def get_incoming_friend_requests_list(self, flag: bool = True) -> set:
        if flag:
            self._update_online_status("Get incoming requests")
        return self._incoming_friend_requests

    def get_outcoming_friend_requests_list(self, flag: bool = True) -> set:
        if flag:
            self._update_online_status("Get outcoming friends")
        return self._outcoming_friend_requests

    def get_mutual_friends(self, uid_user, user: Optional['Phystech'] = None):
        self._update_online_status("Get mutual friends")

        if not user:
            user = self._get_phystech_object(uid_user)

        return self._friends.intersection(user._friends)

    def describe_human(self, uid_user):
        self._update_online_status(f"Describe {uid_user}")

        user = self._get_phystech_object(uid_user)

        return user.__str__()

    def accept_friend_request(self, user_uid: int, decision: bool, user: Optional['Phystech'] = None) -> None:
        """
        Accept a friend request
        :param user_uid: int
        :param decision: bool, True - accept, False - reject
        :param user: an Phystech object
        :return: None
        """
        self._update_online_status("Accept friend")

        if not user:
            user = self._get_phystech_object(user_uid)

        if user._get_uid() not in self.get_incoming_friend_requests_list(False):
            print("Such user isn't in your friend requests. Check id one more time")
            return None

        if decision:
            self._friends.add(user._get_uid())
            user._friends.add(self.__uid)

        self._incoming_friend_requests.remove(user._get_uid())
        user._outcoming_friend_requests.remove(self.__uid)

    def block_user(self, user_uid: int, user: Optional['Phystech'] = None) -> None:
        """
        A user can block another user so
        another user can't add friend him

        :param user_uid: int
        :param user: an Phystech object
        :return: None
        """
        self._update_online_status("Block user")

        if not user:
            user = self._get_phystech_object(user_uid)

        assert self != user, "You can\'t block yourself!"

        if user._get_uid() in self.get_block_users_list(False):
            print(f"You've already blocked {user._get_name()}")
        else:
            self._block_users.add(user._get_uid())
            self.remove_friend(user_uid, user, False)
            self.accept_friend_request(user._get_uid(), False, user)
            print(f"You blocked {user._get_name()}")

    def unblock_user(self, user_uid: int, user: Optional['Phystech'] = None, flag: bool = True) -> None:
        """
        Unblock a friend from a black list
        :param user_uid: int
        :param user: optional Phystech object
        :param flag: optional bool
        :return: None
        """

        if flag:
            self._update_online_status("Unblock user")

        if not user:
            user = self._get_phystech_object(user_uid)

        assert self != user, "You can\'t block yourself!"

        if user._get_uid() not in self.get_block_users_list(False):
            if flag:
                print(f"{user._get_name()} isn't blocked")
        else:
            self._block_users.remove(user._get_uid())
            if flag:
                print(f"You're unblocked {user._get_name()}")

    def remove_friend(self, user_uid: int, user: Optional['Phystech'] = None, flag: bool = True) -> None:
        """
        Remove a friend from friends
        :param user_uid: int
        :param user: optional Phystech object
        :param flag: optional flag
        :return:
        """
        self._update_online_status("Remove friend")  # Update online status

        if not user:
            user = self._get_phystech_object(user_uid)

        assert self != user, "You can't remove yourself from  friends!"

        if user._get_uid() not in self.get_friends_list(False):
            if flag:
                print(f"{user._get_name()} isn\'t your friend")
        else:
            self._friends.remove(user._get_uid())
            user._friends.remove(self.__uid)
            print(f'You\' deleted {user._get_name()} from your friends')

    def add_friend(self, user_uid: int, user: Optional['Phystech'] = None) -> None:

        """
        A user can add to his friend list

        :param user_uid: an __uid's object
        :param user: Optional object of Phystech class
        :return: None
        """
        self._update_online_status("Add friend")  # Update online status

        if not user:
            user = self._get_phystech_object(user_uid)

        assert self != user, "You can't add yourself to friends!"

        if self.__uid in user.get_block_users_list(False):
            print(f'You can\'t add {user._get_name()} due to you\'re blocked')
        elif user._get_uid() in self.get_friends_list(False):
            print(f'You\'ve been already a friend of {user._get_name()}')
        elif self.__uid in user.get_incoming_friend_requests_list(False):
            print(f'You\'ve already sent a friend request to {user._get_name()}')
        else:
            self.unblock_user(user._get_uid(), user, False)
            self._outcoming_friend_requests.add(user._get_uid())
            user._incoming_friend_requests.add(self.__uid)
            print('Your request was sent')

        return None

    def __str__(self) -> str:
        str_repr_lines = [
            f'НаФизтехе. Пользователь \"{self.name}\".',
            'День рождения: {}'.format(
                self._birthday if self._birthday is not None else '(скрыт)'
            ),
            f'Статус: \"{self.status}\".',
            f'Последний раз был онлайн {self.last_online}',
        ]
        if self.is_graduate is not None:
            if self.is_graduate:
                str_repr_lines.append(
                    f'Выпускник {self._graduation_year} года'
                )
        return '\n'.join(str_repr_lines)


ov = Phystech(
    name='Овчинкин Владимир Александрович',
    birthday=datetime(year=1946, month=6, day=9),
    status='Знаете, как много надо знать, чтобы понять, как мало мы знаем.',
    login='ovchinkin',
    graduation_year=2021,
    password='general_physics_rules')


piter = Phystech(
    name='Piter Adsad sadsa',
    birthday=datetime(year=2000, month=6, day=9),
    status='Знаете, как много надо знать, чтобы понять, как мало мы знаем.',
    login='ovchinkin',
    graduation_year=2021,
    password='general_physics_rules'
)

john = Phystech(
    name='John Vara',
    birthday=datetime(year=2000, month=6, day=9),
    status='Знаете, как много надо знать, чтобы понять, как мало мы знаем.',
    login='ovchinkin',
    graduation_year=2021,
    password='general_physics_rules',
)
