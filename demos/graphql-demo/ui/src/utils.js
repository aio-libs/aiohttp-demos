import { random } from 'lodash';

export function getUser() {
  let user_id = window.localStorage.getItem('id');

  if (!user_id) {
    user_id = random(1, 10);
    window.localStorage.setItem('id', user_id);
  } else {
    user_id = Number(user_id)
  }

  return user_id
}
