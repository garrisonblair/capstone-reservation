import React from 'react';
import renderer from 'react-test-renderer';
import GroupsRowItem from '../../components/Groups/GroupsRowItem';

function setup(myUserId, groupOwnerId) {
  const syncGroupsList = () => { };
  const group = {
    id: 1,
    name: 'groupName',
    owner: {
      id: groupOwnerId,
    },
  };

  return { syncGroupsList, group, myUserId };
}

it('Shows row as owner', () => {
  const { syncGroupsList, group, myUserId } = setup(1, 1);
  const tree = renderer
    .create(
      <GroupsRowItem
        syncGroupsList={syncGroupsList}
        group={group}
        myUserId={myUserId}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Shows row as member', () => {
  const { syncGroupsList, group, myUserId } = setup(1, 2);
  const tree = renderer
    .create(
      <GroupsRowItem
        syncGroupsList={syncGroupsList}
        group={group}
        myUserId={myUserId}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
