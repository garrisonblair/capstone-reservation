import React from 'react';
import renderer from 'react-test-renderer';
import MemberRowItem from '../../components/Groups/MemberRowItem';


it('Shows row with username as admin', () => {
  const member = { username: 'myusername' };
  const tree = renderer
    .create(
      <MemberRowItem
        member={member}
        isAdmin
        deleteFunction={() => { }}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Shows row with username as non-admin', () => {
  const member = { username: 'myusername' };
  const tree = renderer
    .create(
      <MemberRowItem
        member={member}
        isAdmin={false}
        deleteFunction={() => { }}
      />,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
