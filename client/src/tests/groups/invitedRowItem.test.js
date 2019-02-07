/* eslint-disable no-undef */
import React from 'react';
import renderer from 'react-test-renderer';
import InvitedRowItem from '../../components/Groups/InvitedRowItem';

function setup() {
  const selectedInvitation = {
    id: 1,
    invited_booker: {
      username: 'myUsername',
    },
  };
  const deleteFunction = () => { };

  return { selectedInvitation, deleteFunction };
}

it('Shows row', () => {
  const { selectedInvitation, deleteFunction } = setup();
  const tree = renderer
    .create(
      <InvitedRowItem
        selectedInvitation={selectedInvitation}
        deleteFunction={deleteFunction}
        isAdmin={false}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Shows row as admin', () => {
  const { selectedInvitation, deleteFunction } = setup();
  const tree = renderer
    .create(
      <InvitedRowItem
        selectedInvitation={selectedInvitation}
        deleteFunction={deleteFunction}
        isAdmin
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Shows row loading', () => {
  const { selectedInvitation, deleteFunction } = setup();
  const tree = renderer
    .create(
      <InvitedRowItem
        selectedInvitation={selectedInvitation}
        deleteFunction={deleteFunction}
        isAdmin
        isLoadingForTesting
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
