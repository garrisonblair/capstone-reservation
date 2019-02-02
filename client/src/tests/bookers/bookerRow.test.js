/* eslint-disable no-undef */
import React from 'react';
import renderer from 'react-test-renderer';
import BookerRow from '../../components/Admin/Bookers/BookerRow';

function setup() {
  const booker = {
    first_name: 'first',
    last_name: 'last',
    username: 'username',
    email: 'test@email.com',
    booker_profile: {
      privilege_categories: [],
    },
  };
  const syncBookers = () => { };

  return { booker, syncBookers };
}

it('Shows bookers table', () => {
  const { booker, syncBookers } = setup();
  const tree = renderer
    .create(
      <BookerRow
        booker={booker}
        syncBookers={syncBookers}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
