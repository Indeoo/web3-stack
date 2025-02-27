from sybil_engine.module.module import Module
from sybil_engine.utils.accumulator import add_accumulator, get_value

from web3_wizzard_lib.core.utils.statistic_utils import statistic_date_string, get_statistic_writer
from web3_wizzard_lib.utils.debank_utils import debank_request

TOTAL_USD = "TotalUSD"
DEBANK_ACC_NUM = "DEBANK_ACC_NUM"


class DebankChecker(Module):
    module_name = "DEBANK_CHECKER"
    module_config = None

    cumulative_chain_sums = {}

    supported_chains = [
        'ethereum',
        'arbitrum',
        'op',
        'zksync era',
        'base',
        'bnb Chain',
        'linea',
        'polygon',
        'avalanche',
        'scroll',
        'utils',
        'fantom',
        'zora',
        'arbitrum nova',
        'celo',
        'klaytn'
    ]

    def execute(self, account, statistic_write='GOOGLE'):
        data = debank_request(account.address)

        job_name = f"debank_{statistic_date_string}"
        statistics_writer = get_statistic_writer()

        add_accumulator(DEBANK_ACC_NUM, 1)

        total_usd_value = data.get('total_usd_value', 0)
        chain_list = data.get('chain_list', [])
        chain_list = [item for item in chain_list if item['name'].lower() in self.supported_chains]
        chain_list = sorted(chain_list, key=lambda x: x['community_id'])

        chain_names = [chain.get('name') for chain in chain_list]

        statistics_writer.init_if_required(
            job_name,
            ['ADS ID', 'Wallet ID', 'Total USD Value'] + chain_names
        )

        row = [account.app_id, account.address, total_usd_value]
        for chain in chain_list:
            usd_value = chain.get('usd_value', 0)
            row.append(usd_value)

            if chain['name'] in self.cumulative_chain_sums:
                self.cumulative_chain_sums[chain['name']] += usd_value
            else:
                self.cumulative_chain_sums[chain['name']] = usd_value

        statistics_writer.write_row(job_name, row)

        add_accumulator(TOTAL_USD, total_usd_value)

        if get_value(DEBANK_ACC_NUM) == get_value("Acc Amount"):
            cumulative_row = ['SUM', '', get_value(TOTAL_USD)]
            for chain_name in chain_names:
                cumulative_row.append(self.cumulative_chain_sums.get(chain_name, 0))

            statistics_writer.write_row(job_name, cumulative_row)

    def log(self):
        return "Debank Checker"
